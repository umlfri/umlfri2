from ..base import Command as Command
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.model import DiagramDeletedEvent as DiagramDeletedEvent
from typing import Iterator
from umlfri2.application.events.model.diagramdeleted import DiagramDeletedEvent
from umlfri2.model.diagram import Diagram
from umlfri2.qtgui.rendering.qtruler import QTRuler


class DeleteDiagramCommand(Command):
    def __init__(self, diagram: Diagram) -> None: ...
    @property
    def description(self): ...
    def get_updates(self) -> Iterator[DiagramDeletedEvent]: ...
