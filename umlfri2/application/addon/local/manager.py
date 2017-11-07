import os.path

from umlfri2.application.events.addon import AddOnInstalledEvent
from umlfri2.constants.paths import ADDONS, LOCAL_ADDONS
from umlfri2.datalayer.loaders import AddOnListLoader
from umlfri2.datalayer.storages import DirectoryStorage

from .actions import AddOnStarter, AddOnStopper


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
    
    def install_addon(self, storage):
        if self.__local_addons is None:
            if not os.path.exists(LOCAL_ADDONS):
                os.makedirs(LOCAL_ADDONS)
            self.__local_addons = AddOnListLoader(self.__application, DirectoryStorage.new_storage(LOCAL_ADDONS), False)
        
        addon = self.__local_addons.install_from(storage)
        if addon is None:
            raise Exception("Cannot install addon")
        
        self.__addons.append(addon)
        self.__application.event_dispatcher.dispatch(AddOnInstalledEvent(addon))
    
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
