from typing import Optional
from umlfri2.model.element.elementobject import ElementObject


class ElementCreatedEvent:
    def __init__(
        self,
        element: ElementObject,
        index: None = ...,
        indirect: bool = ...
    ) -> None: ...
    @property
    def element(self) -> ElementObject: ...
    @property
    def index(self) -> None: ...
    @property
    def indirect(self) -> bool: ...
