from .local import AddOnManager
from .online import OnlineAddOnManager


class AddOnList:
    def __init__(self, application):
        self.__local = AddOnManager(application)
        self.__online = OnlineAddOnManager(application)
    
    def init(self):
        self.__local.load_addons()
    
    @property
    def local(self):
        return self.__local
    
    @property
    def online(self):
        return self.__online
