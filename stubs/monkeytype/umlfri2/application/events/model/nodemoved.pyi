from umlfri2.model.element.elementobject import ElementObject


class NodeMovedEvent:
    def __init__(
        self,
        node: ElementObject,
        old_parent: ElementObject,
        old_index: int,
        new_parent: ElementObject,
        new_index: int
    ) -> None: ...
    @property
    def new_index(self) -> int: ...
    @property
    def new_parent(self) -> ElementObject: ...
    @property
    def node(self) -> ElementObject: ...
    @property
    def old_parent(self) -> ElementObject: ...
