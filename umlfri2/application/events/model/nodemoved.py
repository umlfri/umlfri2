from __future__ import annotations

from typing import Union, TYPE_CHECKING

from ..base import Event

if TYPE_CHECKING:
    from umlfri2.model import ElementObject, Diagram, Project


class NodeMovedEvent(Event):
    def __init__(self, node: Union[ElementObject, Diagram], old_parent: Union[ElementObject, Project],
                 old_index: int, new_parent: Union[ElementObject, Project], new_index: int) -> None:
        self.__node = node
        self.__old_parent = old_parent
        self.__old_index = old_index
        self.__new_parent = new_parent
        self.__new_index = new_index
    
    @property
    def node(self) -> Union[ElementObject, Diagram]:
        return self.__node
    
    @property
    def old_parent(self) -> Union[ElementObject, Project]:
        return self.__old_parent
    
    @property
    def old_index(self) -> int:
        return self.__old_index
    
    @property
    def new_parent(self) -> Union[ElementObject, Project]:
        return self.__new_parent
    
    @property
    def new_index(self) -> int:
        return self.__new_index
    
    def get_opposite(self) -> NodeMovedEvent:
        return NodeMovedEvent(self.__node, self.__new_parent, self.__new_index, self.__old_parent, self.__old_index)
