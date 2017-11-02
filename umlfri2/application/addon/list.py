from .local import AddOnManager

class AddOnList:
    def __init__(self, application):
        self.__local = AddOnManager(application)
    
    def init(self):
        self.__local.load_addons()
    
    @property
    def local(self):
        return self.__local
