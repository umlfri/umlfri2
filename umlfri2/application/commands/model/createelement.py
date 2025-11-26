from __future__ import annotations

from typing import Iterator, Optional, TYPE_CHECKING, Union

from umlfri2.application.events.model import ElementCreatedEvent
from ..base import Command

if TYPE_CHECKING:
    from umlfri2.application.events.base import Event
    from umlfri2.metamodel.elementtype import ElementType
    from umlfri2.model import ElementObject, Project
    from umlfri2.ufl.components.visual.canvas import Ruler


class CreateElementCommand(Command):
    def __init__(self, parent: Union[ElementObject, Project], element_type: ElementType) -> None:
        self.__parent = parent
        self.__element_type = element_type
        self.__element_object = None
    
    @property
    def description(self) -> str:
        return "Creating element '{0}'".format(self.__element_type.id)
    
    def _do(self, ruler: Ruler) -> None:
        self.__element_object = self.__parent.create_child_element(self.__element_type)
    
    def _redo(self, ruler: Ruler) -> None:
        self.__parent.add_child(self.__element_object)
    
    def _undo(self, ruler: Ruler) -> None:
        self.__parent.remove_child(self.__element_object)
    
    @property
    def element_object(self) -> Optional[ElementObject]:
        return self.__element_object
    
    def get_updates(self) -> Iterator[Event]:
        yield ElementCreatedEvent(self.__element_object)
