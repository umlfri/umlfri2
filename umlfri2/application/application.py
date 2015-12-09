import ctypes
import locale
import os

from umlfri2.addon import AddOnManager
from umlfri2.application.commands.solution import NewProjectCommand
from umlfri2.application.events.solution import OpenSolutionEvent, SaveSolutionEvent
from umlfri2.application.tablist import TabList
from umlfri2.datalayer import Storage
from umlfri2.datalayer.loaders import ProjectLoader, WholeSolutionLoader
from umlfri2.datalayer.savers import WholeSolutionSaver
from umlfri2.datalayer.storages import ZipStorage
from umlfri2.model import Solution
from umlfri2.paths import ADDONS
from umlfri2.types.version import Version
from .dispatcher import EventDispatcher
from .commandprocessor import CommandProcessor


class MetaApplication(type):
    __instance = None
    
    def __call__(cls):
        if cls.__instance is None:
            cls.__instance = type.__call__(cls)
        
        return cls.__instance


class Application(metaclass=MetaApplication):
    VERSION = Version("2.0")
    NAME = "UML .FRI"

    def __init__(self):
        self.__event_dispatcher = EventDispatcher()
        self.__commands = CommandProcessor(self)
        with Storage.read_storage(ADDONS) as addon_storage:
            self.__addons = AddOnManager(addon_storage)
        self.__tabs = TabList(self)
        self.__solution = None
        self.__ruler = None
        self.__solution_storage_ref = None
        self.__language = self.__find_out_language()

    def __find_out_language(self):
        for e in 'LANGUAGE', 'LC_ALL', 'LC_MESSAGES', 'LANG':
            if e in os.environ:
                return os.environ[e]

        if os.name == 'nt':
            langid = ctypes.windll.kernel32.GetUserDefaultUILanguage()
            return locale.windows_locale[langid]

        lang, enc = locale.getlocale()
        if lang is not None:
            return lang

        lang, enc = locale.getlocale()
        if lang is not None:
            return lang

        return 'POSIX'
    
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
    
    @property
    def solution_name(self):
        if self.__solution_storage_ref is None:
            return None
        else:
            return self.__solution_storage_ref.name
    
    def new_project(self, template, new_solution=True, project_name="Project"):
        if new_solution:
            project = ProjectLoader(template.load(), self.__ruler, True, project_name, addon=template.addon).load()
            self.__solution = Solution(project)
            self.__solution_storage_ref = None
            self.__commands.clear_buffers()
            self.__commands.mark_unchanged()
            self.__event_dispatcher.dispatch(OpenSolutionEvent(self.__solution))
            self.tabs.close_all()
        else:
            command = NewProjectCommand(self.__solution, template, project_name)
            self.__commands.execute(command)
    
    @property
    def should_save_as(self):
        return self.__solution_storage_ref is None
    
    @property
    def can_save_solution(self):
        return self.__solution is not None and self.unsaved
    
    def save_solution(self):
        if self.__solution_storage_ref is None:
            raise Exception
        
        with self.__solution_storage_ref.open(mode='w') as storage:
            WholeSolutionSaver(storage, self.__ruler).save(self.__solution)
        
        self.__commands.mark_unchanged()
        
        self.__event_dispatcher.dispatch(SaveSolutionEvent(self.__solution))
    
    @property
    def can_save_solution_as(self):
        return self.__solution is not None
    
    def save_solution_as(self, filename):
        with ZipStorage.new_storage(filename) as storage:
            WholeSolutionSaver(storage, self.__ruler).save(self.__solution)
            self.__solution_storage_ref = storage.remember_reference()
        
        self.__commands.mark_unchanged()
        
        self.__event_dispatcher.dispatch(SaveSolutionEvent(self.__solution))

    def open_solution(self, filename):
        with Storage.read_storage(filename) as storage:
            self.__solution = WholeSolutionLoader(storage, self.__ruler, self.__addons).load()
            self.__solution_storage_ref = storage.remember_reference()
        
        self.__commands.clear_buffers()
        self.__commands.mark_unchanged()
        self.__event_dispatcher.dispatch(OpenSolutionEvent(self.__solution))
        self.tabs.close_all()
    
    @property
    def language(self):
        return self.__language
