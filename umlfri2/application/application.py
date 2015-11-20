from umlfri2.addon import AddOnManager
from umlfri2.application.tablist import TabList
from umlfri2.datalayer.storages import Storage
from umlfri2.paths import ADDONS
from .dispatcher import EventDispatcher
from .commandprocessor import CommandProcessor


class MetaApplication(type):
    __instance = None
    
    def __call__(cls):
        if cls.__instance is None:
            cls.__instance = type.__call__(cls)
        
        return cls.__instance


class Application(metaclass=MetaApplication):
    def __init__(self):
        self.__event_dispatcher = EventDispatcher()
        self.__commands = CommandProcessor(self)
        self.__addons = AddOnManager(Storage.create_storage(ADDONS))
        self.__tabs = TabList(self)
        self.__solution = None
        self.__ruler = None
    
    def use_ruler(self, ruler):
        if self.__ruler is not None:
            raise Exception("Cannot change used ruler")
        self.__ruler = ruler
    
    @property
    def ruler(self):
        return self.__ruler
    
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
    
    @property
    def tabs(self):
        return self.__tabs
    
    @solution.setter
    def solution(self, value):
        self.__solution = value
