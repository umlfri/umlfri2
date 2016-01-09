import inspect
import threading
import traceback

from collections import Iterable

from ..interfaces import IApplication, Interface


class PluginExecutor(object):
    def __init__(self, channel):
        self.__channel = channel
        application = IApplication(self)
        self.__objects = { # TODO: replace with weakref.WeakValueDictionary
            application.id: application
        }
    
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
            target = self.__objects[data['target']]
            selector = data['selector']
            arguments = data.get('arguments', {})
            
            method = getattr(target, selector)
            
            arguments = self.__decode_parameters(method, arguments)
            ret = method(**arguments)
            
            if session is not None:
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
                vartype, value = value
                # TODO: exception - incorrect parameter type
                if vartype == "boolean":
                    typed_parameters[name] = value == "true"
                elif vartype == "int32":
                    typed_parameters[name] = int(value)
                elif vartype == "float":
                    typed_parameters[name] = float(value)
                elif vartype == "string":
                    typed_parameters[name] = str(value)
                else:
                    pass # TODO: exception - incorrect type
            else:
                # TODO: exception - incorrect parameter type
                typed_parameters[name] = type(value)
        
        # TODO: exception - some parameters left unprocessed
        
        return typed_parameters
    
    def __encode_return(self, method, ret):
        polymorfic = hasattr(method, 'method_polymorfic')

        def recursion(ret):
            if not isinstance(ret, str) and isinstance(ret, Iterable):
                return [recursion(value) for value in ret]
            elif isinstance(ret, Interface):
                if ret.id not in self.__objects:
                    self.__objects[ret.id] = ret
                if polymorfic:
                    return ret.type, ret.id
                else:
                    return ret.id
            else:
                return ret
        
        return recursion(ret)
    
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
