import os.path
import uuid

from .starter import AddOnStarter
from .stopper import AddOnStopper
from umlfri2.constants.paths import ADDONS, LOCAL_ADDONS
from umlfri2.datalayer import AddOnLoader, Storage
from umlfri2.datalayer.storages import DirectoryStorage


class AddOnManager:
    def __init__(self, application):
        self.__addons = []
        self.__application = application
    
    def load_addons(self):
        with Storage.read_storage(ADDONS) as addon_storage:
            self.__load_addons_from_storage(addon_storage, True)
        if os.path.exists(LOCAL_ADDONS):
            with Storage.read_storage(LOCAL_ADDONS) as addon_storage:
                self.__load_addons_from_storage(addon_storage, False)
    
    def __load_addons_from_storage(self, storage, system_location):
        for dir in storage.list():
            with storage.create_substorage(dir) as addon_storage:
                self.__append_addon_from_storage(addon_storage, system_location)

    def __append_addon_from_storage(self, addon_storage, system_addon):
        loader = AddOnLoader(self.__application, addon_storage, system_addon)
        if loader.is_addon() and loader.is_enabled():
            self.__addons.append(loader.load())

    def install_addon(self, storage):
        if not os.path.exists(LOCAL_ADDONS):
            os.makedirs(LOCAL_ADDONS)
        
        dir_name = str(uuid.uuid1())
        with DirectoryStorage.new_storage(LOCAL_ADDONS) as addon_storage:
            with addon_storage.make_dir(dir_name) as destination_storage:
                destination_storage.copy_from(storage)
                self.__append_addon_from_storage(destination_storage, False)
    
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
