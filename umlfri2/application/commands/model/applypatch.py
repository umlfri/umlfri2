from __future__ import annotations

from typing import Any, Iterator, List, Tuple, TYPE_CHECKING, Union

from umlfri2.application.events.model import ObjectDataChangedEvent
from umlfri2.model import ElementObject
from umlfri2.ufl.objects.patch import UflObjectPatch
from ..base import Command, CommandNotDone

if TYPE_CHECKING:
    from umlfri2.application.events.base import Event
    from umlfri2.model import ConnectionObject
    from umlfri2.model.element import ElementVisual
    from umlfri2.types.geometry import Size
    from umlfri2.ufl.components.visual.canvas import Ruler


class ApplyPatchCommand(Command):
    def __init__(self, object: Union[ElementObject, ConnectionObject], patch: UflObjectPatch) -> None:
        self.__object = object
        self.__patch = patch
        self.__visual_sizes = []
    
    @property
    def description(self) -> str:
        if isinstance(self.__object, ElementObject):
            name = "element {0}".format(self.__object.get_display_name())
        else:
            name = "connection"
        
        change = self.__patch.get_lonely_change()
        is_object_patch = isinstance(self.__patch, UflObjectPatch)
        if change is not None and is_object_patch:
            change_desc = "property {0}".format(change.name)
        else:
            change_desc = "properties"
        
        return "Changed {0} of {1}".format(change_desc, name)

    def _do(self, ruler: Ruler) -> None:
        if not self.__patch.has_changes:
            raise CommandNotDone
        
        if isinstance(self.__object, ElementObject):
            for visual in self.__object.visuals:
                self.__visual_sizes.append((visual, visual.get_size(ruler)))
        
        self.__object.apply_ufl_patch(self.__patch)

    def _redo(self, ruler: Ruler) -> None:
        self.__object.apply_ufl_patch(self.__patch)
    
    def _undo(self, ruler: Ruler) -> None:
        self.__object.apply_ufl_patch(self.__patch.make_reverse())
        
        for visual, size in self.__visual_sizes:
            visual.resize(ruler, size)
    
    def get_updates(self) -> Iterator[Event]:
        yield ObjectDataChangedEvent(self.__object, self.__patch)
