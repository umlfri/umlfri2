from ..base import Command as Command
from ..diagram import HideElementsCommand as HideElementsCommand
from _typeshed import Incomplete
from collections.abc import Generator
from typing import NamedTuple
from umlfri2.application.events.model import ConnectionDeletedEvent as ConnectionDeletedEvent, DiagramDeletedEvent as DiagramDeletedEvent, ElementDeletedEvent as ElementDeletedEvent

class DeletedElementDescription(NamedTuple):
    index: Incomplete
    element: Incomplete

class DeletedDiagramDescription(NamedTuple):
    index: Incomplete
    diagram: Incomplete

class DeleteElementsCommand(Command):
    def __init__(self, elements) -> None: ...
    @property
    def description(self): ...
    def get_updates(self) -> Generator[Incomplete, Incomplete]: ...
