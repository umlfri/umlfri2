import os.path
from configparser import ConfigParser

from umlfri2.constants.paths import CONFIG


class ApplicationConfig:
    CONFIG_FILE = os.path.join(CONFIG, 'umlfri2.ini')
    
    def __init__(self):
        self.__language = None
        
        if os.path.exists(self.CONFIG_FILE):
            self.__load()
    
    @property
    def language(self):
        return self.__language
    
    @language.setter
    def language(self, value):
        self.__language = value
        
        self.__save()
    
    def __load(self):
        cp = ConfigParser()

        cp.read(self.CONFIG_FILE)
        
        self.__language = cp.get('Language', 'code', fallback=None)
    
    def __save(self):
        if not os.path.exists(CONFIG):
            os.makedirs(CONFIG)
        
        cp = ConfigParser()
        
        if self.__language is not None:
            cp.add_section('Language')
            cp.set('Language', 'code', self.__language)

        with open(self.CONFIG_FILE, 'w') as cf:
            cp.write(cf)
