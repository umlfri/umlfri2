from umlfri2.addon import AddOnManager
from umlfri2.application.commands.solution import NewProjectCommand
from umlfri2.application.events.solution import OpenSolutionEvent
from umlfri2.application.tablist import TabList
from umlfri2.datalayer import Storage
from umlfri2.datalayer.loaders import ProjectLoader
from umlfri2.datalayer.savers import WholeSolutionSaver
from umlfri2.datalayer.storages import ZipStorage
from umlfri2.model import Solution
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
        self.__solution_storage_ref = None
    
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
    
    @property
    def unsaved(self):
        return self.__commands.changed or (self.__solution is not None and self.__solution_storage_ref is None)
    
    @property
    def templates(self):
        for addon in self.__addons:
            if addon.metamodel is not None:
                yield from addon.metamodel.templates
    
    def new_project(self, template, new_solution=True):
        if new_solution:
            project = ProjectLoader(template.load(), self.__ruler, True, addon=template.addon).load()
            self.__solution = Solution(project)
            self.__event_dispatcher.dispatch(OpenSolutionEvent(self.__solution))
            self.__solution_storage_ref = None
            self.__commands.clear_buffers()
            self.__commands.mark_unchanged()
        else:
            command = NewProjectCommand(self.__solution, template)
            self.__commands.execute(command)
    
    @property
    def should_save_as(self):
        return self.__solution_storage_ref is None
    
    @property
    def can_save_project(self):
        return self.__solution is not None and self.unsaved
    
    def save_project(self):
        if self.__solution_storage_ref is None:
            raise Exception
        
        with self.__solution_storage_ref.open() as storage:
            WholeSolutionSaver(storage, self.__ruler).save(self.__solution)
        
        self.__commands.mark_unchanged()
    
    @property
    def can_save_project_as(self):
        return self.__solution is not None
    
    def save_project_as(self, filename):
        with ZipStorage.new_storage(filename) as storage:
            WholeSolutionSaver(storage, self.__ruler).save(self.__solution)
            self.__solution_storage_ref = storage.remember_reference()
        
        self.__commands.mark_unchanged()
