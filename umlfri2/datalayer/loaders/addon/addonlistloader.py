import re

import os.path

import lxml.etree
import unicodedata

from ...constants import ADDON_ADDON_FILE
from .addoninfoloader import AddOnInfoLoader
from .addonloader import AddOnLoader


class AddOnListLoader:
    __RE_INVALID_CHARACTER_GROUP = re.compile('[^a-zA-Z0-9]+')
    
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
    
    def install_from(self, storage, validator_callback=None):
        path = None
        for file in storage.get_all_files():
            if os.path.basename(file) == ADDON_ADDON_FILE:
                path = os.path.dirname(file)
        
        if path is None:
            raise Exception("Selected file is not an addon")
        
        with storage.create_substorage(path) as source_storage:
            info = AddOnInfoLoader(lxml.etree.parse(source_storage.open(ADDON_ADDON_FILE)).getroot()).load()
            
            if validator_callback is not None:
                if not validator_callback(info):
                    raise Exception("Invalid add-on")
            
            dir_name = self.__mk_unique_dir_name(info.identifier)
            
            with self.__storage.make_dir(dir_name) as destination_storage:
                destination_storage.copy_from(source_storage)
                return self.__load(destination_storage)
    
    def __mk_unique_dir_name(self, identifier):
        dir_name = ''.join(char for char in unicodedata.normalize('NFD', identifier)
                           if unicodedata.category(char) != 'Mn')
        dir_name = self.__RE_INVALID_CHARACTER_GROUP.sub('-', dir_name)
        
        if self.__storage.exists(dir_name):
            format = dir_name + "-{0}"
            i = 1
            while self.__storage.exists(format.format(i)):
                i += 1
            dir_name = format.format(i)
        
        return dir_name
    
    def __load(self, addon_storage):
        loader = AddOnLoader(self.__application, addon_storage, self.__system_location)
        if loader.is_addon() and loader.is_enabled():
            return loader.load()
        return None
