from umlfri2.addon import AddOnManager
from umlfri2.datalayer.storages import Storage
from umlfri2.paths import ADDONS
from .dispatcher import EventDispatcher
from .commandprocessor import CommandProcessor


class Application:
    def __init__(self):
        self.__event_dispatcher = EventDispatcher()
        self.__commands = CommandProcessor(self.__event_dispatcher)
        self.__addons = AddOnManager(Storage.open(ADDONS))
        self.__solution = None
    
    @property
    def event_dispatcher(self):
        return self.__event_dispatcher
    
    @property
    def commands(self):
        return self.__commands
    
    @property
    def solution(self):
        return self.__solution
    
    @property
    def addons(self):
        return self.__addons
    
    @solution.setter
    def solution(self, value):
        self.__solution = value
