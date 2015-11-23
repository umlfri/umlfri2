from ..base import Event


class RemoveProjectEvent(Event):
    def __init__(self, project):
        self.__project = project
    
    @property
    def project(self):
        return self.__project
    
    def get_opposite(self):
        from .openproject import OpenProjectEvent
        
        return OpenProjectEvent(self.__project)
