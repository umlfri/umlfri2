import os.path
from configparser import ConfigParser

from umlfri2.constants.paths import CONFIG
from umlfri2.types.version import Version


class ApplicationConfig:
    CONFIG_FILE = os.path.join(CONFIG, 'umlfri2.ini')
    
    def __init__(self):
        self.__language = None
        self.__ignored_version = None
        
        if os.path.exists(self.CONFIG_FILE):
            self.__load()
    
    @property
    def language(self):
        return self.__language
    
    @language.setter
    def language(self, value):
        self.__language = value
        
        self.__save()
    
    @property
    def ignored_version(self):
        return self.__ignored_version
    
    @ignored_version.setter
    def ignored_version(self, value):
        self.__ignored_version = value
        
        self.__save()

    def __load(self):
        cp = ConfigParser()

        cp.read(self.CONFIG_FILE)
        
        self.__language = cp.get('Language', 'code', fallback=None)
        ignored_version = cp.get('Updates', 'ignored_version', fallback=None)
        if ignored_version is None:
            self.__ignored_version = None
        else:
            self.__ignored_version = Version(ignored_version)
    
    def __save(self):
        if not os.path.exists(CONFIG):
            os.makedirs(CONFIG)
        
        cp = ConfigParser()
        
        if self.__language is not None:
            cp.add_section('Language')
            cp.set('Language', 'code', self.__language)
        
        if self.__ignored_version is not None:
            cp.add_section('Updates')
            cp.set('Updates', 'ignored_version', str(self.__ignored_version))

        with open(self.CONFIG_FILE, 'w') as cf:
            cp.write(cf)
