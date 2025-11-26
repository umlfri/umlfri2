from __future__ import annotations

from typing import Iterator, List, TYPE_CHECKING

from umlfri2.application.events.solution import OpenProjectEvent
from umlfri2.model import ProjectBuilder
from ..base import Command

if TYPE_CHECKING:
    from umlfri2.application.events.base import Event
    from umlfri2.model import Solution, Project
    from umlfri2.model.builder import StartupTab
    from umlfri2.metamodel.projecttemplate import ProjectTemplate
    from umlfri2.ufl.components.visual.canvas import Ruler


class NewProjectCommand(Command):
    def __init__(self, solution: Solution, template: ProjectTemplate, project_name: str) -> None:
        self.__template_id = template.id
        self.__project_name = project_name
        self.__solution = solution
        self.__template = template
        self.__project = None
        self.__tabs = []
    
    @property
    def description(self) -> str:
        return "Creating a new project from template '{0}'".format(self.__template_id)
    
    def _do(self, ruler: Ruler) -> None:
        builder = ProjectBuilder(ruler, self.__template, self.__project_name)
        self.__project = builder.project
        self.__tabs = list(builder.tabs)
        
        self._redo(ruler)
    
    def _redo(self, ruler: Ruler) -> None:
        self.__solution.add_project(self.__project)
    
    def _undo(self, ruler: Ruler) -> None:
        self.__solution.remove_project(self.__project)
    
    @property
    def opened_tabs(self) -> Iterator[StartupTab]:
        yield from self.__tabs
    
    def get_updates(self) -> Iterator[Event]:
        yield OpenProjectEvent(self.__project)
