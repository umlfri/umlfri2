import os

import subprocess

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
        
        env['UMLFRI_PIN'] = str(channel.child_reader_handle)
        env['UMLFRI_POUT'] = str(channel.child_writer_handle)
        
        self.__process = subprocess.Popen(program, close_fds = False, env = env)
        
        channel.close_child_descriptors()
        
        return channel
    
    def terminate(self):
        try:
            self.__process.terminate()
        except IOError:
            if self.__process.poll() is None:
                raise
    
    def kill(self):
        try:
            self.__process.kill()
        except IOError:
            if self.__process.poll() is None:
                raise
    
    @property
    def is_alive(self):
        return self.__process.poll() is None
