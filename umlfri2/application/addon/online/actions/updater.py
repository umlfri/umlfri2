from itertools import chain

from .downloader import OnlineAddonVersionDownloader


class OnlineAddOnUpdater:
    def __init__(self, local_manager, *addon_versions):
        self.__local_manager = local_manager
        self.__addon_versions = addon_versions
        self.__error = False
        self.__finished = False
        self.__downloaders = None
    
    def combine_with(self, other):
        return OnlineAddOnUpdater(self.__local_manager, *chain(other.__addon_versions, self.__addon_versions))
    
    @property
    def finished(self):
        return self.__finished
    
    @property
    def has_error(self):
        return self.__error
    
    def do(self):
        if self.__downloaders is None:
            self.__downloaders = [OnlineAddonVersionDownloader(v) for v in self.__addon_versions]
        
        downloaded = []
        to_download = []
        for downloader in self.__downloaders:
            if downloader.downloaded:
                downloaded.append(downloader)
            else:
                to_download.append(downloader)
        
        self.__downloaders[:] = to_download

        if not any(self.__downloaders):
            self.__finished = True # TODO: install update
