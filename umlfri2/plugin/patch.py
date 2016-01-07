import re
import sys
import types


class PatchPlugin:
    __RE_MODULE_NAME_INVALID_CHAR = re.compile('[^a-zA-Z0-9]')
    
    def __init__(self, addon_path, module):
        self.__addon_path = addon_path
        self.__module = module
        
        self.__addon = None
        self.__obj = None
    
    def _set_addon(self, addon):
        self.__addon = addon
    
    def __load_patch(self):
        if 'plugins' not in sys.modules:
            sys.modules['plugins'] = types.ModuleType('plugins')
        
        module_name = self.__RE_MODULE_NAME_INVALID_CHAR.sub('_', self.__addon.identifier)
        
        addon_fqn = 'plugins.%s'%module_name
        patch_fqn = 'plugins.%s.%s'%(module_name, self.__module)
        
        if addon_fqn not in sys.modules:
            module = sys.modules[addon_fqn] = types.ModuleType(module_name)
            module.__path__ = [self.__addon_path]
            
            setattr(sys.modules['plugins'], module_name, module)
        
        module = __import__(patch_fqn)
        module = getattr(module, module_name)
        module = getattr(module, self.__module)
        
        self.__obj = module.Patch()
    
    def start(self):
        if self.__obj is None:
            self.__load_patch()
        
        if self.__obj is not None:
            self.__obj.start()
    
    def stop(self):
        if self.__obj is not None:
            self.__obj.stop()
