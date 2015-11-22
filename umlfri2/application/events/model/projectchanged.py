from ..base import Event


class ProjectChangedEvent(Event):
    def __init__(self, project):
        self.__project = project
    
    @property
    def project(self):
        return self.__project
    
    def get_opposite(self):
        return self
