import os
import os.path

from umlfri2.application.config import ApplicationConfig
from .language import LanguageManager
from .about import AboutUmlFri
from .addon import AddOnManager
from .commands.solution import NewProjectCommand
from .events.application import ItemSelectedEvent, ClipboardSnippetChangedEvent
from .events.solution import OpenSolutionEvent, SaveSolutionEvent, CloseSolutionEvent
from .startupoptions import StartupOptions
from .tablist import TabList
from .commandprocessor import CommandProcessor
from .dispatcher import EventDispatcher
from .recentfiles import RecentFiles

from umlfri2.datalayer import Storage
from umlfri2.datalayer.loaders import ProjectLoader, WholeSolutionLoader
from umlfri2.datalayer.savers import WholeSolutionSaver
from umlfri2.datalayer.storages import ZipStorage
from umlfri2.model import Solution


class MetaApplication(type):
    __instance = None
    
    def __call__(cls):
        if cls.__instance is None:
            cls.__instance = type.__call__(cls)
        
        return cls.__instance


class Application(metaclass=MetaApplication):
    def __init__(self):
        self.__event_dispatcher = EventDispatcher(self)
        self.__commands = CommandProcessor(self)
        
        self.__addons = AddOnManager(self)
        
        self.__addons.load_addons()
        
        self.__recent_files = RecentFiles(self)
        
        self.__tabs = TabList(self)
        self.__solution = None
        self.__ruler = None
        self.__solution_storage_ref = None
        self.__selected_item = None
        self.__clipboard = None
        self.__thread_manager = None
        self.__startup_options = None
        
        self.__config = ApplicationConfig()
        self.__language = LanguageManager(self)

        self.__about = AboutUmlFri(self)
    
    @property
    def about(self):
        return self.__about
    
    def start(self):
        self.__startup_options.apply()
    
    def stop(self):
        self.__event_dispatcher.clear()

    def use_args(self, args):
        self.__startup_options = StartupOptions(self, args)
    
    def use_ruler(self, ruler):
        if self.__ruler is not None:
            raise Exception("Cannot change used ruler")
        self.__ruler = ruler
    
    def use_thread_manager(self, thread_manager):
        if self.__thread_manager is not None:
            raise Exception("Cannot change used thread manager")
        self.__thread_manager = thread_manager
    
    @property
    def ruler(self):
        return self.__ruler
    
    @property
    def thread_manager(self):
        return self.__thread_manager
    
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
    def recent_files(self):
        yield from self.__recent_files
    
    @property
    def solution_name(self):
        if self.__solution_storage_ref is None:
            return None
        else:
            return self.__solution_storage_ref.name
    
    def new_project(self, template, new_solution=True, project_name="Project"):
        if new_solution:
            self.__event_dispatcher.dispatch(CloseSolutionEvent(self.__solution))
            project = ProjectLoader(template.load(), self.__ruler, True, project_name, addon=template.addon).load()
            self.__solution = Solution(project)
            self.__solution_storage_ref = None
            self.__commands.clear_buffers()
            self.__commands.mark_unchanged()
            self.__event_dispatcher.dispatch(OpenSolutionEvent(self.__solution))
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
        
        self.__recent_files.add_file(filename)

    def open_solution(self, filename):
        filename = os.path.abspath(filename)
        with Storage.read_storage(filename) as storage:
            self.__solution = WholeSolutionLoader(storage, self.__ruler, self.__addons).load()
            self.__solution_storage_ref = storage.remember_reference()
        
        self.__commands.clear_buffers()
        self.__commands.mark_unchanged()
        self.__event_dispatcher.dispatch(OpenSolutionEvent(self.__solution))
        self.tabs.close_all()
        self.select_item(None)
        
        self.__recent_files.add_file(filename)
    
    @property
    def language(self):
        return self.__language
    
    @property
    def config(self):
        return self.__config
    
    @property
    def selected_item(self):
        return self.__selected_item
    
    def select_item(self, element):
        if self.__selected_item is not element:
            self.__selected_item = element
            self.__event_dispatcher.dispatch(ItemSelectedEvent(element))
    
    @property
    def clipboard_empty(self):
        if self.__clipboard is None:
            return True
        if self.__clipboard.empty:
            return True
        return False
    
    @property
    def clipboard(self):
        return self.__clipboard
    
    @clipboard.setter
    def clipboard(self, value):
        if self.__clipboard is not value:
            self.__clipboard = value
            self.__event_dispatcher.dispatch(ClipboardSnippetChangedEvent(value))
