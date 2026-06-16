from ..base import Command as Command
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.model import ElementCreatedEvent as ElementCreatedEvent
from typing import Iterator
from umlfri2.application.events.model.elementcreated import ElementCreatedEvent
from umlfri2.metamodel.elementtype import ElementType
from umlfri2.model.element.elementobject import ElementObject
from umlfri2.qtgui.rendering.qtruler import QTRuler


class CreateElementCommand(Command):
    def __init__(
        self,
        parent: ElementObject,
        element_type: ElementType
    ) -> None: ...
    @property
    def description(self): ...
    @property
    def element_object(self): ...
    def get_updates(self) -> Iterator[ElementCreatedEvent]: ...
