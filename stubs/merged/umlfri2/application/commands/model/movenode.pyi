from ..base import Command as Command, CommandNotDone as CommandNotDone
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.model import NodeMovedEvent as NodeMovedEvent
from typing import Iterator
from umlfri2.application.events.model.nodemoved import NodeMovedEvent
from umlfri2.model.element.elementobject import ElementObject
from umlfri2.qtgui.rendering.qtruler import QTRuler


class MoveNodeCommand(Command):
    def __init__(
        self,
        node: ElementObject,
        new_parent: ElementObject,
        new_index: int
    ) -> None: ...
    @property
    def description(self): ...
    def get_updates(self) -> Iterator[NodeMovedEvent]: ...
