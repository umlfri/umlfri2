from ..base import Command as Command
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.model import DiagramCreatedEvent as DiagramCreatedEvent
from typing import Iterator
from umlfri2.application.events.model.diagramcreated import DiagramCreatedEvent
from umlfri2.metamodel.diagramtype import DiagramType
from umlfri2.model.diagram import Diagram
from umlfri2.model.element.elementobject import ElementObject
from umlfri2.qtgui.rendering.qtruler import QTRuler


class CreateDiagramCommand(Command):
    def __init__(
        self,
        parent: ElementObject,
        diagram_type: DiagramType
    ) -> None: ...
    @property
    def description(self): ...
    @property
    def diagram(self) -> Diagram: ...
    def get_updates(self) -> Iterator[DiagramCreatedEvent]: ...
