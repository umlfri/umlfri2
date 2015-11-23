from .projectsaver import ProjectSaver
from .solutionsaver import SolutionSaver


class WholeSolutionSaver:
    def __init__(self, storage, ruler):
        self.__storage = storage
        self.__ruler = ruler
    
    def save(self, solution):
        SolutionSaver(self.__storage, 'solution.xml').save(solution)
        
        for project in solution.children:
            ProjectSaver(self.__storage, 'projects/{0}'.format(project.save_id), self.__ruler).save(project)
