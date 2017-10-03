from umlfri2.application.events.solution import OpenProjectEvent
from umlfri2.model import ProjectBuilder
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
        builder = ProjectBuilder(self.__template)
        self.__project = builder.project
        
        self._redo(ruler)
    
    def _redo(self, ruler):
        self.__solution.add_project(self.__project)
    
    def _undo(self, ruler):
        self.__solution.remove_project(self.__project)
    
    def get_updates(self):
        yield OpenProjectEvent(self.__project)
