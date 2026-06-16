from ..base import Command as Command
from _typeshed import Incomplete
from collections.abc import Generator
from typing import NamedTuple
from umlfri2.application.events.diagram import ConnectionHiddenEvent as ConnectionHiddenEvent, ElementHiddenEvent as ElementHiddenEvent
from typing import (
    Iterator,
    List,
    Tuple,
    Union,
)
from umlfri2.application.events.diagram.connectionhidden import ConnectionHiddenEvent
from umlfri2.application.events.diagram.elementhidden import ElementHiddenEvent
from umlfri2.model.diagram import Diagram
from umlfri2.model.element.elementvisual import ElementVisual
from umlfri2.qtgui.rendering.qtruler import QTRuler


class HiddenVisualDescription(NamedTuple):
    z_order: Incomplete
    visual: Incomplete

class HideElementsCommand(Command):
    def __init__(
        self,
        diagram: Diagram,
        elements: Union[List[ElementVisual], Tuple[ElementVisual]]
    ) -> None: ...
    @property
    def description(self): ...
    def get_updates(
        self
    ) -> Iterator[Union[ElementHiddenEvent, ConnectionHiddenEvent]]: ...
