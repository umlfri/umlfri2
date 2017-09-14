import os.path
from configparser import ConfigParser

from .events.application import RecentFilesChangedEvent
from .recentfile import RecentFile

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
            path = cp.get('File.{}'.format(no), 'path', fallback=None)
            if path is None:
                path = cp.get('Recent Files', str(no), fallback=None)
            if path is not None:
                self.__files.append(RecentFile(self.__application, self, path))
    
    def __save(self):
        if not os.path.exists(CONFIG):
            os.makedirs(CONFIG)
        
        cp = ConfigParser()
        cp.add_section('Recent Files')
        
        cp.set('Recent Files', 'count', str(len(self.__files)))
        
        for no, file in enumerate(self.__files):
            cp.add_section('File.{}'.format(no))
            cp.set('File.{}'.format(no), 'path', file.path)
        
        with open(self.CONFIG_FILE, 'w') as cf:
            cp.write(cf)
    
    def __iter__(self):
        yield from self.__files

    def _remove(self, file):
        self.__files.remove(file)
        
        self.__save()

        self.__application.event_dispatcher.dispatch(RecentFilesChangedEvent(file))
    
    def add_file(self, file_path):
        self.__files = [file for file in self.__files if file.path != file_path]

        self.__files.append(RecentFile(self.__application, self, file_path))
        
        if len(self.__files) > 10:
            del self.__files[10:]
        
        self.__save()
        
        self.__application.event_dispatcher.dispatch(RecentFilesChangedEvent(file_path))
