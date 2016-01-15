import sys

from ..message import Message
from ...main_loops.default import DefaultMainLoop
from ..factory import Factory

from threading import Lock


class Server:
    def __init__(self, channel):
        self.__channel = channel
        self.__stopped = False
        
        self.__main_loop = None
        
        self.__factory = Factory(self)
        
        self.__message_lock = Lock()
        self.__messages = {}
        self.__session_id = 0
        self.__events = {}
    
    @property
    def factory(self):
        return self.__factory
    
    def start(self, main_loop=None):
        if main_loop is None:
            self.__main_loop = DefaultMainLoop()
        else:
            self.__main_loop = main_loop
        
        self.__main_loop.start(self.__serve)
    
    def main_loop(self):
        self.__main_loop.main_loop()
        if not self.__channel.closed:
            self.__channel.write(
                {
                    'target': 'system',
                    'selector': 'stopped'
                }
            )
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
    
    def connect_event(self, target, selector, registrar_api_name, handler):
        key = target, selector
        
        if key in self.__events:
            self.__events[key].append(handler)
        else:
            Message(target, registrar_api_name).send_async(self)
            self.__events[key] = [handler]
    
    def disconnect_event(self, target, selector, deregistrar_api_name, handler):
        key = target, selector
        
        if key not in self.__events or handler not in self.__events[key]:
            raise Exception("Event handler not connected to the event")
        
        self.__events[key].remove(handler)
        if not self.__events[key]:
            Message(target, deregistrar_api_name).send_async(self)
            del self.__events[key]
    
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
            else:
                self.__fire_event(data['target'], data['selector'], data.get('arguments', {}))
    
    def __fire_event(self, target, selector, arguments):
        key = target, selector
        
        if key in self.__events:
            for handler in self.__events[key]:
                try:
                    self.__main_loop.call(handler, arguments)
                except Exception as ex:
                    sys.excepthook(ex.__class__, ex, ex.__traceback__)
