import os.path

from umlfri2.application.events.addon import AddOnInstalledEvent, AddOnUninstalledEvent
from umlfri2.constants.paths import ADDONS, LOCAL_ADDONS
from umlfri2.datalayer.loaders import AddOnListLoader
from umlfri2.datalayer.storages import DirectoryStorage

from .actions import AddOnStarter, AddOnStopper
from .state import AddOnState


class AddOnManager:
    def __init__(self, application):
        self.__addons = []
        self.__application = application
        self.__system_addons = AddOnListLoader(application, DirectoryStorage.read_storage(ADDONS), True)
        if os.path.exists(LOCAL_ADDONS):
            self.__local_addons = AddOnListLoader(self.__application, DirectoryStorage.new_storage(LOCAL_ADDONS), False)
        else:
            self.__local_addons = None
    
    def load_addons(self):
        self.__addons.clear()
        self.__addons.extend(self.__system_addons.load_all())
        if self.__local_addons is not None:
            self.__addons.extend(self.__local_addons.load_all())
    
    def install_addon(self, storage, online_addon_version):
        if self.__local_addons is None:
            if not os.path.exists(LOCAL_ADDONS):
                os.makedirs(LOCAL_ADDONS)
            self.__local_addons = AddOnListLoader(self.__application, DirectoryStorage.new_storage(LOCAL_ADDONS), False)
        
        addon = self.__local_addons.install_from(storage, online_addon_version)
        if addon is None:
            raise Exception("Cannot install add-on")
        
        self.__addons.append(addon)
        self.__application.event_dispatcher.dispatch(AddOnInstalledEvent(addon))
        
        return addon
    
    def install_addon_update(self, storage, online_addon_version):
        return online_addon_version.addon.local_addon # TODO
    
    def uninstall_addon(self, addon):
        if addon.is_system_addon:
            raise Exception("Cannot uninstall system add-on")
        
        if addon.state not in (AddOnState.stopped, AddOnState.error, AddOnState.none):
            raise Exception("Cannot uninstall started add-on")
        
        with addon.storage_reference.open('w') as storage:
            try:
                # try disabling the addon first - just to make sure, it can be disabled if it will be needed
                storage.store_string('.disabled', '')
                storage.remove_storage()
            except:
                try:
                    # if the addon cannot be removed completely, just disable it
                    storage.store_string('.disabled', '')
                except:
                    pass
                raise
        
        self.__addons.remove(addon)
        
        self.__application.event_dispatcher.dispatch(AddOnUninstalledEvent(addon))
    
    def get_addon(self, identifier):
        for addon in self.__addons:
            if addon.identifier == identifier:
                return addon
    
    def start_all(self):
        return AddOnStarter(self, *self.__addons)
    
    def stop_all(self):
        return AddOnStopper(self, *self.__addons)
    
    def __iter__(self):
        yield from self.__addons
