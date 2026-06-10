from typing import Iterator
from umlfri2.metamodel.projecttemplate.project import ProjectTemplate
from umlfri2.model.project import Project
from umlfri2.qtgui.rendering.qtruler import QTRuler


class ProjectBuilder:
    def __init__(
        self,
        ruler: QTRuler,
        template: ProjectTemplate,
        name: str = ...
    ) -> None: ...
    @property
    def project(self) -> Project: ...
    @property
    def tabs(self) -> Iterator[StartupTab]: ...
