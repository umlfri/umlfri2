from ..base import Command as Command, CommandNotDone as CommandNotDone
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.model import ProjectChangedEvent as ProjectChangedEvent
from typing import Iterator
from umlfri2.application.events.model.projectchanged import ProjectChangedEvent
from umlfri2.model.project import Project
from umlfri2.qtgui.rendering.qtruler import QTRuler


class ChangeProjectNameCommand(Command):
    def __init__(self, project: Project, name: str) -> None: ...
    @property
    def description(self): ...
    def get_updates(self) -> Iterator[ProjectChangedEvent]: ...
