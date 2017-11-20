import os.path
from configparser import ConfigParser
from itertools import chain

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
        
        cp.read(self.CONFIG_FILE, encoding='utf8')
        
        count = cp.getint('Recent Files', 'count')
        
        for no in range(count):
            path = cp.get('File.{}'.format(no), 'path', fallback=None)
            if path is None:
                path = cp.get('Recent Files', str(no), fallback=None)
            if path is not None:
                pinned = cp.getboolean('File.{}'.format(no), 'pinned', fallback=False)
                
                self.__files.append(RecentFile(self.__application, self, path, pinned=pinned))
    
    def __save(self):
        if not os.path.exists(CONFIG):
            os.makedirs(CONFIG)
        
        cp = ConfigParser()
        cp.add_section('Recent Files')
        
        cp.set('Recent Files', 'count', str(len(self.__files)))
        
        for no, file in enumerate(self.__files):
            cp.add_section('File.{}'.format(no))
            cp.set('File.{}'.format(no), 'path', file.path)
            
            if file.pinned:
                cp.set('File.{}'.format(no), 'pinned', 'yes')
        
        with open(self.CONFIG_FILE, 'w', encoding='utf8') as cf:
            cp.write(cf)
    
    def __iter__(self):
        yield from self.__files

    def _remove(self, file):
        self.__files.remove(file)
        
        self.__save()

        self.__application.event_dispatcher.dispatch(RecentFilesChangedEvent(file))
    
    def _pin_changed(self, file):
        self.__reorder()
        self.__save()
    
    def __reorder(self):
        self.__files = list(chain(
            (file for file in self.__files if file.pinned),
            (file for file in self.__files if not file.pinned),
        ))
    
    def add_file(self, file_path):
        old_files = [file for file in self.__files if file.path == file_path]
        
        pinned = False
        for file in old_files:
            self.__files.remove(file)
            
            if file.pinned:
                pinned = True
        
        new_file = RecentFile(self.__application, self, file_path, pinned=pinned)
        
        self.__files.insert(0, new_file)
        self.__reorder()
        
        if len(self.__files) > 10:
            del self.__files[10:]
        
        self.__save()
        
        self.__application.event_dispatcher.dispatch(RecentFilesChangedEvent(file_path))
