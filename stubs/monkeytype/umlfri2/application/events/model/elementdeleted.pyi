from typing import Optional
from umlfri2.model.element.elementobject import ElementObject


class ElementDeletedEvent:
    def __init__(
        self,
        element: ElementObject,
        index: Optional[int] = ...,
        indirect: bool = ...
    ) -> None: ...
    @property
    def element(self) -> ElementObject: ...
    @property
    def indirect(self) -> bool: ...
