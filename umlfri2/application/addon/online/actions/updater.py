from functools import partial
from itertools import chain

from .downloader import OnlineAddonVersionDownloader


class OnlineAddOnUpdater:
    def __init__(self, local_manager, *addon_versions):
        self.__local_manager = local_manager
        self.__addon_versions = addon_versions
        self.__error = False
        self.__finished = False
        self.__initialized = False
        self.__downloaders = []
        self.__stoppers = []
        self.__starters = []
    
    def combine_with(self, other):
        return OnlineAddOnUpdater(self.__local_manager, *chain(other.__addon_versions, self.__addon_versions))
    
    @property
    def finished(self):
        return self.__finished
    
    @property
    def has_error(self):
        return self.__error
    
    def do(self):
        if self.__error or self.__finished:
            return
        
        if not self.__initialized:
            self.__stoppers[:] = ((addon_version, addon_version.addon.local_addon.stop())
                                                    for addon_version in self.__addon_versions)
            self.__initialized = True
        
        for starter in self.__starters:
            if starter.has_error:
                self.__error = True
                return
            if not starter.finished:
                starter.do()
        
        if not self.__stoppers and not self.__downloaders and all(starter.finished for starter in self.__starters):
            self.__finished = True
            return
        
        to_stop = []
        for addon_version, stopper in self.__stoppers:
            stopper.do()
            if stopper.has_error:
                self.__error = True
                return
            if stopper.finished:
                self.__downloaders.append(OnlineAddonVersionDownloader(addon_version))
            else:
                to_stop.append((addon_version, stopper))
        
        self.__stoppers[:] = to_stop
        
        downloaded = []
        to_download = []
        for downloader in self.__downloaders:
            if downloader.downloaded:
                downloaded.append(downloader)
            else:
                to_download.append(downloader)
        
        self.__downloaders[:] = to_download

        for downloader in downloaded:
            try:
                addon = self.__local_manager.install_addon_update(
                    downloader.storage,
                    downloader.addon_version
                )
            except:
                self.__error = True
                raise
            
            self.__starters.append(addon.start())
