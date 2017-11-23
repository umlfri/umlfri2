from .downloader import OnlineAddonVersionDownloader


class OnlineAddOnInstaller:
    def __init__(self, local_manager, addon_version):
        if addon_version.addon.local_addon is not None:
            raise Exception("Add-on already installed")
        
        self.__local_manager = local_manager
        self.__addon_version = addon_version
        self.__downloader = None
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
        elif self.__downloader is None:
            self.__downloader = OnlineAddonVersionDownloader(self.__addon_version)
        elif self.__downloader.downloaded:
            try:
                addon = self.__local_manager.install_addon(
                    self.__downloader.storage,
                    self.__addon_version
                )
            except:
                self.__error = True
                raise
            
            self.__starter = addon.start()
