from ..constants import FRIP2_SOLUTION_FILE, FRIP2_PROJECT_FILE, FRIP2_MIMETYPE_FILE, FRIP2_VERSION_FILE, \
    MODEL_SAVE_VERSION, SOLUTION_MIME_TYPE
from .projectsaver import ProjectSaver
from .solutionsaver import SolutionSaver


class WholeSolutionSaver:
    def __init__(self, storage, ruler):
        self.__storage = storage
        self.__ruler = ruler
    
    def save(self, solution):
        self.__storage.store_string(FRIP2_MIMETYPE_FILE, SOLUTION_MIME_TYPE)
        self.__storage.store_string(FRIP2_VERSION_FILE, str(MODEL_SAVE_VERSION))
        
        SolutionSaver(self.__storage, FRIP2_SOLUTION_FILE).save(solution)
        
        for project in solution.children:
            ProjectSaver(self.__storage, FRIP2_PROJECT_FILE.format(project.save_id), self.__ruler).save(project)
