import lxml.etree

from umlfri2.application.addon.guiinjection import GuiInjection
from .toolbarloader import ToolBarLoader
from umlfri2.datalayer.storages import DirectoryStorage
from umlfri2.plugin import PatchPlugin, Plugin
from .metamodelloader import MetamodelLoader
from umlfri2.types.image import Image
from .addoninfoloader import AddOnInfoLoader
from umlfri2.application.addon import AddOn
from ..constants import ADDON_NAMESPACE, ADDON_ADDON_FILE, ADDON_DISABLE_FILE


class AddOnLoader:
    def __init__(self, application, storage, system_addon):
        self.__storage = storage
        self.__application = application
        self.__system_addon = system_addon
    
    def is_addon(self):
        return self.__storage.exists(ADDON_ADDON_FILE)
    
    def is_enabled(self):
        return not self.__storage.exists(ADDON_DISABLE_FILE)
    
    def load(self):
        info = AddOnInfoLoader(lxml.etree.parse(self.__storage.open(ADDON_ADDON_FILE)).getroot()).load()
        
        metamodel = None
        if info.metamodel:
            with self.__storage.create_substorage(info.metamodel) as metamodel_storage:
                metamodel = MetamodelLoader(metamodel_storage, self.__storage, info).load()
        
        if info.icon is None:
            icon = None
        else:
            if not self.__storage.exists(info.icon):
                raise Exception("Unknown icon {0}".format(info.icon))
            icon = Image(self.__storage, info.icon)
        
        toolbars = []
        actions = {}
        for toolbar_path in info.toolbars:
            toolbars.append(
                ToolBarLoader(
                    self.__application,
                    self.__storage,
                    lxml.etree.parse(self.__storage.open(toolbar_path)).getroot(),
                    actions
                ).load()
            )
        
        gui_injection = GuiInjection(actions, toolbars)
        
        if info.patch_module is None:
            patch = None
        else:
            if not isinstance(self.__storage, DirectoryStorage):
                raise Exception
            patch = PatchPlugin(self.__storage.path, info.patch_module)
        
        if info.plugin_info is None:
            plugin = None
        else:
            if not isinstance(self.__storage, DirectoryStorage):
                raise Exception
            plugin = Plugin(self.__storage.path, info.plugin_info.starter, info.plugin_info.path)
        
        ret = AddOn(self.__application, info.identifier, info.name, info.version, info.author, info.homepage,
                    info.license, icon, info.description, info.requirements, info.provisions, info.config,
                    metamodel, gui_injection, patch, plugin, self.__system_addon)
        
        ret.compile()
        
        return ret
