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


class HideElementsCommand:
    def __init__(
        self,
        diagram: Diagram,
        elements: Union[List[ElementVisual], Tuple[ElementVisual]]
    ) -> None: ...
    def _do(self, ruler: QTRuler) -> None: ...
    def _redo(self, ruler: QTRuler) -> None: ...
    def get_updates(
        self
    ) -> Iterator[Union[ElementHiddenEvent, ConnectionHiddenEvent]]: ...
