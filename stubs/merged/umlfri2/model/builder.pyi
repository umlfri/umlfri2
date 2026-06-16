from .project import Project as Project
from _typeshed import Incomplete
from collections.abc import Generator
from typing import NamedTuple
from umlfri2.metamodel.projecttemplate import DiagramTemplateState as DiagramTemplateState
from umlfri2.ufl.types.enum import UflFlagsType as UflFlagsType
from umlfri2.ufl.types.structured import UflListType as UflListType, UflObjectType as UflObjectType

class StartupTab(NamedTuple):
    diagram: Incomplete
    locked: Incomplete

class ProjectBuilder:
    def __init__(self, ruler, template, name: str = 'Project') -> None: ...
    @property
    def project(self): ...
    @property
    def tabs(self) -> Generator[Incomplete, Incomplete]: ...
