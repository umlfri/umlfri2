from concurrent.futures import ThreadPoolExecutor

from umlfri2.datalayer.storages import ZipStorage

download_executor = ThreadPoolExecutor(max_workers=4)


class OnlineAddOnInstaller:
    def __init__(self, local_manager, addon_version):
        self.__local_manager = local_manager
        self.__addon_version = addon_version
        self.__download_future = None
        self.__error = False
        self.__finished = False
        self.__starter = None
    
    @property
    def finished(self):
        return self.__finished
    
    @property
    def has_error(self):
        return self.__error
    
    def do(self):
        if self.__error or self.__finished:
            return
        
        if self.__starter is not None:
            try:
                self.__starter.do()
            finally:
                self.__error = self.__starter.has_error
                self.__finished = self.__starter.finished
        elif self.__download_future is None:
            self.__download_future = download_executor.submit(self.__download)
        elif self.__download_future.done():
            try:
                storage = ZipStorage.read_from_memory(self.__download_future.result(0))
                addon = self.__local_manager.install_addon(storage, validator_callback=self.__validate_addon_info)
            except:
                self.__error = True
                raise
            
            self.__starter = addon.start()
    
    def __validate_addon_info(self, info):
        if info.identifier != self.__addon_version.addon.identifier:
            return False
        if info.version != self.__addon_version.version:
            return False
        return True
    
    def __download(self):
        location = self.__addon_version.valid_location
        if location is None:
            raise Exception("There is no valid add-on location for current platform")
        return location.download()
