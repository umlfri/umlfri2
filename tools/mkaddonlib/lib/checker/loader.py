import inspect
import os
import pkgutil
import sys
from types import FunctionType

from lib.checker.list import UmlFriInterfaceList
from lib.checker.method import UmlFriInterfaceMethod
from lib.checker.parameter import UmlFriInterfaceMethodParameter
from .interface import UmlFriInterface


class UmlFriInterfaceLoader:
    __app_root = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
    
    def __init__(self):
        sys.path.append(self.__app_root)
        import umlfri2.plugin.interfaces
        self.__interfaces_module = umlfri2.plugin.interfaces
        self.__interface_base = umlfri2.plugin.interfaces.Interface
    
    def load(self):
        return UmlFriInterfaceList(self.__load())

    def __load(self):
        root_module_name = self.__interfaces_module.__name__
        for finder, module_name, is_package in pkgutil.walk_packages(self.__interfaces_module.__path__):
            module = self.__import_module(root_module_name, module_name)
            yield from self.__load_interfaces_from(module)

    def __import_module(self, package_name, module_name):
        module_name = "{0}.{1}".format(package_name, module_name)
        module = __import__(module_name)
        for part in module_name.split(".")[1:]:
            module = getattr(module, part)
        return module
    
    def __load_interfaces_from(self, module):
        for name, value in module.__dict__.items():
            if value == self.__interface_base:
                continue
            if not name.startswith('I'):
                continue
            if not isinstance(value, type):
                continue
            if not issubclass(value, self.__interface_base):
                continue
            
            yield self.__load_interface(value)
    
    def __load_interface(self, interface):
        methods = []
        for name in dir(interface): # get inherited members too
            if name.startswith('_'):
                continue
            
            if name == 'id':
                continue
            
            value = getattr(interface, name)
            
            if isinstance(value, FunctionType):
                methods.append(self.__load_method(value))
        
        name = interface.__name__[1:] # strip I from the interface name
        return UmlFriInterface(name, methods)
    
    def __load_method(self, method):
        spec = inspect.getfullargspec(method)
        
        params = []
        
        for name in spec.args:
            if name == 'self':
                continue
            
            type = spec.annotations[name]
            
            params.append(UmlFriInterfaceMethodParameter(name, type))
        
        polymorfic = False
        if 'return' in spec.annotations:
            if spec.annotations['return'] is object:
                polymorfic = True
        
        name = method.__name__
        return UmlFriInterfaceMethod(name, params, polymorfic)
