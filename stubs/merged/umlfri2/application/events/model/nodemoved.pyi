from ..base import Event as Event
from umlfri2.model.element.elementobject import ElementObject


class NodeMovedEvent(Event):
    def __init__(
        self,
        node: ElementObject,
        old_parent: ElementObject,
        old_index: int,
        new_parent: ElementObject,
        new_index: int
    ) -> None: ...
    @property
    def node(self) -> ElementObject: ...
    @property
    def old_parent(self) -> ElementObject: ...
    @property
    def old_index(self): ...
    @property
    def new_parent(self) -> ElementObject: ...
    @property
    def new_index(self) -> int: ...
    def get_opposite(self): ...
