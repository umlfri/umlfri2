from ...main_loops.default import DefaultMainLoop
from ..factory import Factory

from threading import Lock


class Server:
    def __init__(self, channel):
        self.__channel = channel
        self.__stopped = False
        
        self.__main_loop = DefaultMainLoop()
        
        self.__factory = Factory(self)
        
        self.__message_lock = Lock()
        self.__messages = {}
        self.__session_id = 0
    
    @property
    def factory(self):
        return self.__factory
    
    def set_main_loop(self, main_loop):
        if self.__main_loop.in_main_loop:
            raise Exception("Cannot change main loop while plugin is running")
        self.__main_loop = main_loop
    
    def main_loop(self):
        self.__main_loop.main_loop(self.__serve)
        self.__main_loop.wait()
    
    def send_command(self, message, async=False):
        if self.__stopped:
            raise ValueError('Communication with server was closed')
        
        with self.__message_lock:
            encoded = message.create_message()
            
            if not async:
                self.__session_id += 1
                self.__messages[self.__session_id] = message
                encoded['session'] = self.__session_id
            
            self.__channel.write(encoded)
    
    def __serve(self):
        while not self.__stopped:
            data = self.__channel.read()
            
            if self.__channel.closed:
                return
            
            msg = None
            with self.__message_lock:
                if 'session' in data:
                    session_id = data['session']
                    if session_id in self.__messages:
                        msg = self.__messages[session_id]
                        del self.__messages[session_id]
            
            if msg is None:
                self.__accept(data)
            else:
                msg.accept(data)
    
    def __accept(self, data):
        if 'target' in data:
            if data['target'] == 'system' and data['selector'] == 'stop':
                self.__channel.close()
                self.__main_loop.quit()
                self.__stopped = True
            # TODO: event handling
