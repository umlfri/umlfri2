import os

import subprocess

import signal

try:
    import msvcrt
except ImportError:
    pass

from .starter import PluginStarter
from ..communication import PipeChannel


class BaseProgramStarter(PluginStarter):
    program = ()
    environment = {}
    
    def __init__(self, path):
        self.__path = path
    
    def start(self):
        channel = PipeChannel()
        
        env = os.environ.copy()
        
        for name, value in self.environment.items():
            env['UMLFRI_' + name] = value.format(path = self.__path)
        
        program = [part.format(path = self.__path) for part in self.program]
        
        if os.name == 'nt':
            ppin = msvcrt.get_osfhandle(channel.child_reader_descriptor)
            ppout = msvcrt.get_osfhandle(channel.child_writer_descriptor)
            
            env['UMLFRI_PIN'] = str(ppin)
            env['UMLFRI_POUT'] = str(ppout)
            
            self.__process = subprocess.Popen(program, close_fds = False, env = env)
            channel.close_child_descriptors()
        else:
            env['UMLFRI_PIN'] = str(channel.child_reader_descriptor)
            env['UMLFRI_POUT'] = str(channel.child_writer_descriptor)
            pid = os.fork()
            if pid:
                #parent
                self.__pid = pid
                channel.close_child_descriptors()
            else:
                #child
                channel.close()
                os.execve(program[0], program, env)
        
        return channel
    
    def terminate(self):
        if os.name == 'nt':
            try:
                self.__process.terminate()
            except IOError:
                if self.__process.poll() is None:
                    raise

        else:
            os.kill(self.__pid, signal.SIGTERM)
        
    def kill(self):
        if os.name == 'nt':
            try:
                self.__process.kill()
            except IOError:
                if self.__process.poll() is None:
                    raise
        else:
            os.kill(self.__pid, signal.SIGKILL)
    
    @property
    def is_alive(self):
        if os.name == 'nt':
            return self.__process.poll() is None
        else:
            try:
                return os.waitpid(self.__pid, os.WNOHANG) == (0, 0)
            except:
                return False
