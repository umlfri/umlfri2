import os.path
from configparser import ConfigParser

from umlfri2.constants.paths import CONFIG
from umlfri2.types.version import Version


class ApplicationConfig:
    CONFIG_FILE = os.path.join(CONFIG, 'umlfri2.ini')
    
    def __init__(self):
        self.__language = None
        self.__ignored_versions = []
        self.__auto_check_updates = True
        
        if os.path.exists(self.CONFIG_FILE):
            self.__load()
    
    @property
    def language(self):
        return self.__language
    
    @language.setter
    def language(self, value):
        if self.__language == value:
            return
        
        self.__language = value
        
        self.__save()
    
    @property
    def ignored_versions(self):
        yield from self.__ignored_versions
    
    def ignore_version(self, version):
        if version in self.__ignored_versions:
            return
        
        self.__ignored_versions.append(version)
        
        self.__save()
    
    def unignore_versions(self, *versions):
        if versions and not all(ver in self.__ignored_versions for ver in versions):
            return
        
        for ver in versions:
            self.__ignored_versions.remove(ver)
        
        self.__save()
    
    @property
    def auto_check_updates(self):
        return self.__auto_check_updates
    
    @auto_check_updates.setter
    def auto_check_updates(self, value):
        if self.__auto_check_updates == value:
            return
        
        self.__auto_check_updates = value
        
        self.__save()
    
    def __load(self):
        cp = ConfigParser()

        cp.read(self.CONFIG_FILE, encoding='utf8')
        
        self.__language = cp.get('Language', 'code', fallback=None)
        
        ignored_versions = cp.get('Updates', 'ignored_versions', fallback='')
        self.__ignored_versions = [Version(ver) for ver in ignored_versions.split()]
        
        self.__auto_check_updates = cp.getboolean('Updates', 'check_on_startup', fallback=True)
    
    def __save(self):
        if not os.path.exists(CONFIG):
            os.makedirs(CONFIG)
        
        cp = ConfigParser()
        
        cp.add_section('Language')
        
        if self.__language is None:
            # comment out the option
            cp.set('Language', '; code', '')
        else:
            cp.set('Language', 'code', self.__language)
        
        cp.add_section('Updates')
        
        if self.__auto_check_updates:
            cp.set('Updates', 'check_on_startup', 'yes')
        else:
            cp.set('Updates', 'check_on_startup', 'no')
        
        cp.set('Updates', 'ignored_versions', ' '.join(str(ver) for ver in self.__ignored_versions))
        
        with open(self.CONFIG_FILE, 'w', encoding='utf8') as cf:
            cp.write(cf)
