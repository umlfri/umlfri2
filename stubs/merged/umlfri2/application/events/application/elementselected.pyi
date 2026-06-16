from ..base import Event as Event
from typing import (
    Optional,
    Union,
)
from umlfri2.model.diagram import Diagram
from umlfri2.model.element.elementobject import ElementObject
from umlfri2.model.project import Project


class ItemSelectedEvent(Event):
    def __init__(
        self,
        item: Optional[Union[Diagram, ElementObject, Project]]
    ) -> None: ...
    @property
    def item(
        self
    ) -> Optional[Union[Diagram, ElementObject, Project]]: ...
