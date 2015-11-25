from umlfri2.application.events.solution import OpenProjectEvent
from umlfri2.datalayer.loaders import ProjectLoader
from ..base import Command


class NewProjectCommand(Command):
    def __init__(self, solution, template, project_name):
        self.__template_name = template.name
        self.__project_name = project_name
        self.__solution = solution
        self.__template = template
        self.__project = None
        
    def description(self):
        return "Creating a new project from template '{0}'".format(self.__template_name)
    
    def _do(self, ruler):
        self.__project = ProjectLoader(self.__template.load(), ruler, True, self.__project_name,
                                       addon=self.__template.addon).load()
        
        self._redo(ruler)
    
    def _redo(self, ruler):
        self.__solution.add_project(self.__project)
    
    def _undo(self, ruler):
        self.__solution.remove_project(self.__project)
    
    def get_updates(self):
        yield OpenProjectEvent(self.__project)
