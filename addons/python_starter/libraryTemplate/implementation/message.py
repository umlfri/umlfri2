from threading import Event

from .message_result import MessageResult


class Message(object):
    def __init__(self, target, selector):
        self.__target = target
        self.__selector = selector
        self.__arguments = {}
        self.__send_event = Event()
        self.__result = None
        self.__interrupted = False
    
    def boolean_parameter(self, name, value):
        self.__arguments[name] = bool(value)
        return self
    
    def int32_parameter(self, name, value):
        self.__arguments[name] = int(value)
        return self
    
    def float_parameter(self, name, value):
        self.__arguments[name] = float(value)
        return self
    
    def variant_parameter(self, name, value):
        if not isinstance(value, (int, str, float, bool)):
            raise ValueError
        self.__arguments[name] = value
        return self
    
    def string_parameter(self, name, value):
        if value is not None:
            value = str(value)
        self.__arguments[name] = value
        return self
    
    def xy_parameter(self, name, value):
        self.__arguments[name] = (int(value[0]), int(value[1]))
        return self
    
    def xywh_parameter(self, name, value):
        self.__arguments[name] = (int(value[0]), int(value[1]))
        return self
    
    def wh_parameter(self, name, value):
        self.__arguments[name] = (int(value[0]), int(value[1]), int(value[2]), int(value[3]))
        return self
    
    def object_parameter(self, name, value, is_polymorphic):
        if is_polymorphic:
            self.__arguments[name] = (value.__interface__, value.__id__)
        else:
            self.__arguments[name] = value.__id__
        return self
    
    def args_parameter(self, name, values):
        if not all(isinstance(item, (int, str, float, bool)) for item in values):
            raise ValueError
        self.__arguments[name] = tuple(values)
        return self
    
    def send(self, server):
        server.send_command(self)
        self.__send_event.wait()
        if self.__interrupted:
            raise ValueError('Communication with server was closed')
        return MessageResult(server.factory, self.__result)
    
    def send_async(self, server):
        server.send_command(self, True)
    
    def create_message(self):
        return {'target': self.__target, 'selector': self.__selector, 'arguments': self.__arguments}
    
    def accept(self, data):
        self.__result = data
        self.__send_event.set()
    
    def interrupt(self):
        self.__interrupted = True
        self.__send_event.set()
