from ..base import Command as Command, CommandNotDone as CommandNotDone
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.diagram import ConnectionShownEvent as ConnectionShownEvent, ElementShownEvent as ElementShownEvent
from typing import Iterator
from umlfri2.application.events.diagram.elementshown import ElementShownEvent
from umlfri2.model.diagram import Diagram
from umlfri2.model.element.elementobject import ElementObject
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.geometry.point import Point


class ShowElementCommand(Command):
    def __init__(
        self,
        diagram: Diagram,
        element_object: ElementObject,
        point: Point
    ) -> None: ...
    @property
    def description(self): ...
    @property
    def element_visual(self): ...
    @property
    def element_object(self): ...
    def get_updates(self) -> Iterator[ElementShownEvent]: ...
