import lxml.etree
import os

from umlfri2.datalayer.constants import ONLINE_ADDON_LAST_VERSION_FILE
from .onlineaddonloader import OnlineAddOnLoader


class OnlineAddOnListLoader:
    def __init__(self, application, storage):
        self.__application = application
        self.__storage = storage
    
    def load_all(self):
        parser = lxml.etree.XMLParser(remove_comments=True)
        
        for file in self.__storage.get_all_files():
            if not file.endswith('.xml'):
                continue
            xml = lxml.etree.parse(self.__storage.open(file), parser=parser).getroot()
            loader = OnlineAddOnLoader(self.__application, xml, self.__storage, os.path.dirname(file))
            if not loader.is_valid():
                continue

            yield loader.load()
    
    def get_last_update(self):
        if self.__storage.exists(ONLINE_ADDON_LAST_VERSION_FILE):
            return self.__storage.read_string(ONLINE_ADDON_LAST_VERSION_FILE)
        else:
            return None
