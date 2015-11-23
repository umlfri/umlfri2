from ..base import Event


class OpenProjectEvent(Event):
    def __init__(self, project):
        self.__project = project
    
    @property
    def project(self):
        return self.__project
    
    def get_opposite(self):
        from .removeproject import RemoveProjectEvent
        
        return RemoveProjectEvent(self.__project)
