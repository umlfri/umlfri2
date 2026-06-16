from ..base import Command as Command
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.solution import OpenProjectEvent as OpenProjectEvent
from umlfri2.model import ProjectBuilder as ProjectBuilder
from typing import Iterator
from umlfri2.application.events.solution.openproject import OpenProjectEvent
from umlfri2.metamodel.projecttemplate.project import ProjectTemplate
from umlfri2.model.builder import StartupTab
from umlfri2.model.solution import Solution
from umlfri2.qtgui.rendering.qtruler import QTRuler


class NewProjectCommand(Command):
    def __init__(
        self,
        solution: Solution,
        template: ProjectTemplate,
        project_name: str
    ) -> None: ...
    @property
    def description(self): ...
    @property
    def opened_tabs(self) -> Iterator[StartupTab]: ...
    def get_updates(self) -> Iterator[OpenProjectEvent]: ...
