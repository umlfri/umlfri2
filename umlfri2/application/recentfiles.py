import os.path
from configparser import ConfigParser

from umlfri2.application.events.application import RecentFilesChangedEvent
from umlfri2.constants.paths import CONFIG


class RecentFiles:
    CONFIG_FILE = os.path.join(CONFIG, 'recent.ini')
    
    def __init__(self, application):
        self.__files = []
        self.__application = application
        
        if os.path.exists(self.CONFIG_FILE):
            self.__load()
    
    def __load(self):
        cp = ConfigParser()
        
        cp.read(self.CONFIG_FILE)
        
        count = cp.getint('Recent Files', 'count')
        
        for no in range(count):
            self.__files.append(cp.get('Recent Files', str(no)))
    
    def __save(self):
        if not os.path.exists(CONFIG):
            os.makedirs(CONFIG)
        
        cp = ConfigParser()
        cp.add_section('Recent Files')
        
        cp.set('Recent Files', 'count', str(len(self.__files)))
        
        for no, file in enumerate(self.__files):
            cp.set('Recent Files', str(no), file)
        
        with open(self.CONFIG_FILE, 'w') as cf:
            cp.write(cf)
    
    def __iter__(self):
        yield from self.__files
    
    def add_file(self, file):
        if file in self.__files:
            self.__files.remove(file)
        
        self.__files.append(file)
        
        if len(self.__files) > 10:
            del self.__files[10:]
        
        self.__save()
        
        self.__application.event_dispatcher.dispatch(RecentFilesChangedEvent(file))
