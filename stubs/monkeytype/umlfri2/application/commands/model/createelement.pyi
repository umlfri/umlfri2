from typing import Iterator
from umlfri2.application.events.model.elementcreated import ElementCreatedEvent
from umlfri2.metamodel.elementtype import ElementType
from umlfri2.model.element.elementobject import ElementObject
from umlfri2.qtgui.rendering.qtruler import QTRuler


class CreateElementCommand:
    def __init__(
        self,
        parent: ElementObject,
        element_type: ElementType
    ) -> None: ...
    def _do(self, ruler: QTRuler) -> None: ...
    def get_updates(self) -> Iterator[ElementCreatedEvent]: ...
