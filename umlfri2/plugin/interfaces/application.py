from .interface import Interface


class IApplication(Interface):
    def __init__(self, executor):
        pass
    
    @property
    def id(self):
        return 'app'
