from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen

from umlfri2.datalayer.storages import ZipStorage

download_executor = ThreadPoolExecutor(max_workers=4)


class OnlineAddOnInstaller:
    def __init__(self, local_manager, addon_version):
        self.__local_manager = local_manager
        self.__addon_version = addon_version
        self.__download_future = None
        self.__error = False
        self.__finished = False
    
    @property
    def finished(self):
        return self.__finished
    
    @property
    def has_error(self):
        return self.__error
    
    def do(self):
        if self.__finished:
            return
        
        if self.__download_future is None:
            self.__download_future = download_executor.submit(self.__download)
        elif self.__download_future.done():
            try:
                storage = ZipStorage.read_from_memory(self.__download_future.result(0))
                self.__local_manager.install_addon(storage)
            except:
                self.__error = True
                raise
            self.__finished = True
    
    def __download(self):
        location = self.__addon_version.valid_location
        if location is None:
            raise Exception("There is no valid addon location for current platform")
        return location.download()
