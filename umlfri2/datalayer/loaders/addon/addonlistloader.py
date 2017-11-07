import uuid

import os.path

from .addonloader import AddOnLoader


class AddOnListLoader:
    def __init__(self, application, storage, system_location):
        self.__application = application
        self.__storage = storage
        self.__system_location = system_location
    
    def load_all(self):
        for dir in self.__storage.list():
            with self.__storage.create_substorage(dir) as addon_storage:
                addon = self.__load(addon_storage)
                if addon is not None:
                    yield addon
    
    def install_from(self, storage):
        dir_name = str(uuid.uuid1())
        path = None
        for file in storage.get_all_files():
            if os.path.basename(file) == 'addon.xml':
                path = os.path.dirname(file)
        
        if path is None:
            raise Exception("Selected file is not an addon")
        
        with storage.create_substorage(path) as source_storage:
            with self.__storage.make_dir(dir_name) as destination_storage:
                destination_storage.copy_from(source_storage)
                return self.__load(destination_storage)
    
    def __load(self, addon_storage):
        loader = AddOnLoader(self.__application, addon_storage, self.__system_location)
        if loader.is_addon() and loader.is_enabled():
            return loader.load()
        return None
