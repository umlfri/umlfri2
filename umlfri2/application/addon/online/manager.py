import os.path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen

from umlfri2.constants.paths import ONLINE_ADDONS
from umlfri2.datalayer.loaders.onlineaddons import OnlineAddOnListLoader
from umlfri2.datalayer.savers import OnlineAddOnListSaver
from umlfri2.datalayer.storages import ZipStorage, DirectoryStorage

from .addon import OnlineAddOn

update_executor = ThreadPoolExecutor(max_workers=4)


class OnlineAddOnManager:
    __ADDON_LIST_VERSION = "https://api.github.com/repos/umlfri/addon-list/commits/master"
    __ADDON_LIST_DOWNLOAD = "https://api.github.com/repos/umlfri/addon-list/zipball"
    
    def __init__(self, application):
        self.__application = application
        self.__addons = []
        self.__last_version = None
        self.__load_addons()
        self.update()
    
    def __load_addons(self):
        self.__addons.clear()
        addons = {}
        if os.path.exists(ONLINE_ADDONS):
            with DirectoryStorage.read_storage(ONLINE_ADDONS) as storage:
                loader = OnlineAddOnListLoader(self.__application, storage)
                self.__last_version = loader.get_last_update()
                
                for identifier, version in loader.load_all():
                    addons.setdefault(identifier, []).append(version)
        
        for identifier, versions in addons.items():
            self.__addons.append(OnlineAddOn(self.__application, identifier, versions))
    
    def update(self):
        update_executor.submit(self.__update_list)
    
    def __update_list(self):
        try:
            version_request = Request(self.__ADDON_LIST_VERSION)
            version_request.add_header('Accept', 'application/vnd.github.VERSION.sha')
            version = urlopen(version_request).read().decode('ascii')
            
            if version != self.__last_version:
                zip_data = urlopen(self.__ADDON_LIST_DOWNLOAD).read()
                
                with ZipStorage.read_from_memory(zip_data) as source_zipball:
                    files = source_zipball.list()
                    
                    source_storage = source_zipball.create_substorage(next(files))
                    
                    if not os.path.exists(ONLINE_ADDONS):
                        os.makedirs(ONLINE_ADDONS)
                    
                    with DirectoryStorage.new_storage(ONLINE_ADDONS) as storage:
                        OnlineAddOnListSaver(storage).save(source_storage, version)
                
                self.__last_version = version
        finally:
            self.__load_addons()
    
    def __iter__(self):
        yield from self.__addons
