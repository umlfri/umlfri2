import inspect
import threading
import traceback
from base64 import b64encode
from collections import Iterable

from ..interfaces import IApplication, Interface


class PluginExecutor:
    def __init__(self, addon, channel):
        self.__channel = channel
        self.__addon = addon
        application = IApplication(self)
        self.__objects = {
            application.id: application
        }
    
    @property
    def addon(self):
        return self.__addon
    
    def __main(self):
        while True:
            try:
                data = self.__channel.read()
            except:
                traceback.print_exc()
                data = None
                
            if self.__channel.closed:
                return
            
            if data is not None:
                self.__execute(data)
    
    def __execute(self, data):
        session = data.get('session')
        
        try:
            target = data['target']
            selector = data['selector']
            arguments = data.get('arguments', {})
            
            if self.__execute_special(target, selector, arguments):
                return
            
            method = getattr(self.__objects[target], selector)
            
            arguments = self.__decode_parameters(method, arguments)
            ret = method(**arguments)
            
            if session is not None:
                if ret is None:
                    self.__channel.write({'session': session})
                else:
                    self.__channel.write(
                        {
                            'session': session,
                            'return': self.__encode_return(method, ret)
                        }
                    )
            
        except Exception as ex:
            if session is not None:
                self.__channel.write(
                    {
                        'session': session,
                        'exception': self.__encode_exception(ex)
                    }
                )
                # TODO: remove
                traceback.print_exc()
            elif __debug__:
                traceback.print_exc()
    
    def __execute_special(self, target, selector, arguments):
        if target == 'system' and selector == 'stopped':
            self.send_stop()
            return True
        else:
            return False

    def __decode_parameters(self, method, real_parameters):
        spec = inspect.getfullargspec(method)
        
        # ignore self parameter
        parameters = spec.args[1:]
        parameter_types = spec.annotations
        
        typed_parameters = {}
        
        for name in parameters:
            type = parameter_types[name]
            value = real_parameters.pop(name)
            
            if type is object:
                if value is None:
                    typed_parameters[name] = None
                else:
                    # TODO: exception - object not found
                    typed_parameters[name] = self.__objects[value]
            elif type is None:
                typed_parameters[name] = value # variant does not have to be retyped
            else:
                # TODO: exception - incorrect parameter type
                typed_parameters[name] = type(value)
        
        # TODO: exception - some parameters left unprocessed
        
        return typed_parameters
    
    def __encode_return(self, method, ret):
        spec = inspect.getfullargspec(method)
        polymorphic = 'return' in spec.annotations and spec.annotations['return'] is object

        return self.__encode(ret, polymorphic)
    
    def __encode(self, data, polymorphic):
        if isinstance(data, str):
            return data
        elif isinstance(data, bytes):
            return b64encode(data)
        elif isinstance(data, Iterable):
            return [self.__encode(value, polymorphic) for value in data]
        elif isinstance(data, Interface):
            if data.id not in self.__objects:
                self.__objects[data.id] = data
            if polymorphic:
                return data.type, data.id
            else:
                return data.id
        else:
            return data
    
    def __encode_exception(self, ex):
        return {'type': ex.__class__.__name__}
    
    def fire_event(self, target, selector, **arguments):
        self.__channel.write(
            {
                'target': target.id,
                'selector': selector,
                'arguments': arguments
            }
        )
    
    @property
    def running(self):
        return not self.__channel.closed
    
    def start(self):
        threading.Thread(target = self.__main).start()
    
    def send_stop(self):
        self.__channel.write(
            {
                'target': 'system',
                'selector': 'stop'
            }
        )
    
    def object_removed(self, object):
        del self.__objects[object.id]
