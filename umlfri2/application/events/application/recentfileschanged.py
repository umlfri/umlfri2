from ..base import Event


class RecentFilesChangedEvent(Event):
    def __init__(self, new_file):
        self.__new_file = new_file
    
    @property
    def new_file(self):
        return self.__new_file
