import re
import sys
import types


class PatchPlugin:
    __RE_MODULE_NAME_INVALID_CHAR = re.compile('[^a-zA-Z0-9]')
    
    def __init__(self, addon_path, module):
        self.__addon_path = addon_path
        self.__module_name = module
        
        self.__addon = None
        self.__module = None
        self.__obj = None
    
    def _set_addon(self, addon):
        self.__addon = addon
    
    def __load_patch(self):
        if self.__module is None:
            if 'plugins' not in sys.modules:
                sys.modules['plugins'] = types.ModuleType('plugins')
            
            addon_module_name = self.__RE_MODULE_NAME_INVALID_CHAR.sub('_', self.__addon.identifier)
            
            addon_fqn = 'plugins.%s'%addon_module_name
            patch_fqn = 'plugins.%s.%s'%(addon_module_name, self.__module_name)
            
            if addon_fqn not in sys.modules:
                module = sys.modules[addon_fqn] = types.ModuleType(addon_module_name)
                module.__path__ = [self.__addon_path]
                
                setattr(sys.modules['plugins'], addon_module_name, module)
            
            root = __import__(patch_fqn)
            addon_root = getattr(root, addon_module_name)
            self.__module = getattr(addon_root, self.__module_name)
        
        self.__obj = self.__module.Patch()
    
    def start(self):
        if self.__obj is not None:
            raise Exception
        
        self.__load_patch()
        self.__obj.start()
    
    @property
    def running(self):
        return self.__obj is not None 
    
    def stop(self):
        if self.__obj is None:
            raise Exception
        
        self.__obj.stop()
        self.__obj = None
