import lxml.etree
import os

from .onlineaddonloader import OnlineAddOnLoader


class OnlineAddOnListLoader:
    def __init__(self, storage):
        self.__storage = storage
    
    def load_all(self):
        parser = lxml.etree.XMLParser(remove_comments=True)
        
        for file in self.__storage.get_all_files():
            if not file.endswith('.xml'):
                continue
            xml = lxml.etree.parse(self.__storage.open(file), parser=parser).getroot()
            loader = OnlineAddOnLoader(xml, self.__storage, os.path.dirname(file))
            if not loader.is_valid():
                continue

            yield loader.load()
