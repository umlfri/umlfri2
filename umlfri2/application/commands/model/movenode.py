from __future__ import annotations

from typing import Iterator, Optional, TYPE_CHECKING, Union

from umlfri2.application.events.model import NodeMovedEvent
from ..base import Command, CommandNotDone

if TYPE_CHECKING:
    from umlfri2.application.events.base import Event
    from umlfri2.model import Diagram, ElementObject, Project


class MoveNodeCommand(Command):
    def __init__(self, node: Union[ElementObject, Diagram], new_parent: Union[ElementObject, Project],
                 new_index: int) -> None:
        self.__node_name = node.get_display_name()
        self.__node = node
        self.__new_parent = new_parent
        self.__new_index = new_index
        self.__old_parent: Optional[Union[ElementObject, Project]] = None
        self.__old_index: Optional[int] = None
    
    @property
    def description(self) -> str:
        return "Node {0} moved in the project".format(self.__node_name)

    def _do(self, ruler: object) -> None:
        self.__old_parent = self.__node.parent
        self.__old_index = self.__old_parent.get_child_index(self.__node)
        
        if self.__new_parent is self.__old_parent and self.__new_index == self.__old_index:
            raise CommandNotDone
        
        self.__node.change_parent(self.__new_parent, self.__new_index)

    def _redo(self, ruler: object) -> None:
        self.__node.change_parent(self.__new_parent, self.__new_index)
    
    def _undo(self, ruler: object) -> None:
        self.__node.change_parent(self.__old_parent, self.__old_index)
        
    
    def get_updates(self) -> Iterator[Event]:
        yield NodeMovedEvent(self.__node, self.__old_parent, self.__old_index, self.__new_parent, self.__new_index)
