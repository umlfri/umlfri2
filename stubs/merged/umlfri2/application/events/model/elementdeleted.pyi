from ..base import Event as Event
from typing import Optional
from umlfri2.model.element.elementobject import ElementObject


class ElementDeletedEvent(Event):
    def __init__(
        self,
        element: ElementObject,
        index: Optional[int] = None,
        indirect: bool = False
    ) -> None: ...
    @property
    def element(self) -> ElementObject: ...
    @property
    def index(self): ...
    @property
    def indirect(self) -> bool: ...
    def get_opposite(self): ...
