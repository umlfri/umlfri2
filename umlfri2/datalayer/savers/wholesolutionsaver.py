from ..constants import FRIP2_SOLUTION_FILE, FRIP2_PROJECT_FILE, FRIP2_MIMETYPE_FILE, FRIP2_VERSION_FILE, \
    MODEL_SAVE_VERSION, SOLUTION_MIME_TYPE, FRIP2_LOCKED_TABS_FILE
from .projectsaver import ProjectSaver
from .solutionsaver import SolutionSaver
from .lockedtabssaver import LockedTabsSaver


class WholeSolutionSaver:
    def __init__(self, storage, ruler):
        self.__storage = storage
        self.__ruler = ruler
        self.__solution = None
        self.__locked_tabs = []
    
    @property
    def solution(self):
        return self.__solution
    
    @solution.setter
    def solution(self, value):
        self.__solution = value
    
    @property
    def locked_tabs(self):
        return self.__locked_tabs
    
    def add_locked_tab(self, tab):
        self.__locked_tabs.append(tab)
    
    def save(self):
        self.__storage.store_string(FRIP2_MIMETYPE_FILE, SOLUTION_MIME_TYPE)
        self.__storage.store_string(FRIP2_VERSION_FILE, str(MODEL_SAVE_VERSION))
        
        SolutionSaver(self.__storage, FRIP2_SOLUTION_FILE).save(self.__solution)
        
        for project in self.__solution.children:
            ProjectSaver(self.__storage, FRIP2_PROJECT_FILE.format(project.save_id), self.__ruler).save(project)
        
        if self.__locked_tabs:
            LockedTabsSaver(self.__storage, FRIP2_LOCKED_TABS_FILE).save(self.__locked_tabs)
