from typing import Iterator
from umlfri2.application.events.solution.openproject import OpenProjectEvent
from umlfri2.metamodel.projecttemplate.project import ProjectTemplate
from umlfri2.model.builder import StartupTab
from umlfri2.model.solution import Solution
from umlfri2.qtgui.rendering.qtruler import QTRuler


class NewProjectCommand:
    def __init__(
        self,
        solution: Solution,
        template: ProjectTemplate,
        project_name: str
    ) -> None: ...
    def _do(self, ruler: QTRuler) -> None: ...
    def _redo(self, ruler: QTRuler) -> None: ...
    def get_updates(self) -> Iterator[OpenProjectEvent]: ...
    @property
    def opened_tabs(self) -> Iterator[StartupTab]: ...
