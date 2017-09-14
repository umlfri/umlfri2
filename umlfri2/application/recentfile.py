import os.path

from .events.application import RecentFilesChangedEvent


class RecentFile:
    def __init__(self, application, recent_files, file_path, pinned=False):
        self.__application = application
        self.__recent_files = recent_files
        
        self.__pinned = pinned
        
        self.__file_path = file_path
    
    @property
    def exists(self):
        return os.path.exists(self.__file_path)
    
    @property
    def file_name(self):
        return os.path.basename(self.__file_path)
    
    @property
    def path(self):
        return self.__file_path
    
    @property
    def pinned(self):
        return self.__pinned
    
    def pin(self):
        if not self.__pinned:
            self.__pinned = True
            self.__recent_files._pin_changed(self)
            self.__application.event_dispatcher.dispatch(RecentFilesChangedEvent(self.__file_path))

    def unpin(self):
        if self.__pinned:
            self.__pinned = False
            self.__recent_files._pin_changed(self)
            self.__application.event_dispatcher.dispatch(RecentFilesChangedEvent(self.__file_path))
    
    def remove(self):
        self.__recent_files._remove(self)
    
    def open(self):
        self.__application.open_solution(self.__file_path)
