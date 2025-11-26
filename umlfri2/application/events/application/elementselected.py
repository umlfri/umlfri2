from __future__ import annotations

from typing import TYPE_CHECKING, Union

from ..base import Event

if TYPE_CHECKING:
    from umlfri2.model import Project, ElementObject, ConnectionObject, Diagram


class ItemSelectedEvent(Event):
    """
    Item selected in the project tree.
    """
    
    def __init__(self, item: Union[Project, ElementObject, ConnectionObject, Diagram, None]) -> None:
        self.__item = item
    
    @property
    def item(self) -> Union[Project, ElementObject, ConnectionObject, Diagram, None]:
        return self.__item
