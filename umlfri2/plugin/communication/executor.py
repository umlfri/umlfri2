import inspect
import traceback
import sys
from base64 import b64encode
from collections.abc import Iterable

from ..interfaces import IApplication, Interface, InterfaceException


class PluginExecutor:
    def __init__(self, addon, channel, thread_manager):
        self.__channel = channel
        self.__addon = addon
        self.__thread_manager = thread_manager
        application = IApplication(self)
        self.__objects = {
            application.id: application
        }
    
    @property
    def addon(self):
        return self.__addon
    
    def __main(self):
        try:
            while True:
                try:
                    data = self.__channel.read()
                except:
                    traceback.print_exc()
                    data = None
                    
                if self.__channel.closed:
                    break
                
                if data is not None:
                    self.__execute(data)
        finally:
            self.__addon._plugin_stopped()
    
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
            if __debug__:
                traceback.print_exc()
    
    def __execute_special(self, target, selector, arguments):
        if target == 'system' and selector == 'stopped':
            self.send_stop()
            return True
        elif target == 'system' and selector == 'started':
            self.__addon._plugin_started()
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
                    typed_parameters[name] = self.__objects[value]
            elif type is None:
                typed_parameters[name] = value # variant does not have to be retyped
            else:
                typed_parameters[name] = type(value)
        
        if real_parameters:
            raise Exception('Some parameters left unprocessed {0}'.format(tuple(real_parameters.keys())))
        
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
        ret = {
            'type': ex.__class__.__name__,
            'message': str(ex),
            'traceback': [
                {
                    'file': record[0],
                    'line': record[1],
                    'function': record[2]
                }
                for record in traceback.extract_tb(self.__filter_tb(ex.__traceback__))
            ]
        }
        
        if isinstance(ex, InterfaceException):
            ret['data'] = ex.data
        
        return ret
    
    def __filter_tb(self, tb):
        filename = sys._getframe().f_code.co_filename
        
        def filter_tb_recursive(current):
            if current is None:
                return tb
            if current.tb_frame.f_code.co_filename == filename:
                return filter_tb_recursive(current.tb_next)
            return current
        
        return filter_tb_recursive(tb)
    
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
        self.__thread = self.__thread_manager.start_thread(self.__main)
    
    def send_stop(self):
        self.__channel.write(
            {
                'target': 'system',
                'selector': 'stop'
            }
        )
    
    def object_removed(self, object):
        del self.__objects[object.id]
