import os.path

from umlfri2.constants.paths import ONLINE_ADDONS
from umlfri2.datalayer.loaders.onlineaddons import OnlineAddOnListLoader
from umlfri2.datalayer.storages import Storage

from .addon import OnlineAddOn


class OnlineAddOnManager:
    def __init__(self, application):
        self.__application = application
        self.__addons = []
        self.__load_addons()
    
    def __load_addons(self):
        self.__addons.clear()
        addons = {}
        if os.path.exists(ONLINE_ADDONS):
            with Storage.read_storage(ONLINE_ADDONS) as storage:
                for identifier, version in OnlineAddOnListLoader(storage).load_all():
                    addons.setdefault(identifier, []).append(version)
        
        for identifier, versions in addons.items():
            self.__addons.append(OnlineAddOn(self.__application, identifier, versions))
    
    def __iter__(self):
        yield from self.__addons
