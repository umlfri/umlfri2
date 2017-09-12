import os.path


class RecentFile:
    def __init__(self, application, recent_files, file_path):
        self.__application = application
        self.__recent_files = recent_files
        
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
    
    def remove(self):
        self.__recent_files._remove(self)
    
    def open(self):
        self.__application.open_solution(self.__file_path)
