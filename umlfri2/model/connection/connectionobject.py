from __future__ import annotations

from _weakrefset import WeakSet
from typing import Iterator, Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from weakref import ref
from umlfri2.model.cache import ModelTemporaryDataCache
from umlfri2.ufl.dialog import UflDialog, UflDialogOptions

if TYPE_CHECKING:
    from umlfri2.metamodel.connectiontype import ConnectionType
    from umlfri2.model import ElementObject, Project
    from umlfri2.model.connection import ConnectionVisual
    from umlfri2.ufl.objects import UflObject, UflObjectPatch
    from umlfri2.ufl.components.visual.canvas import Ruler
    from umlfri2.ufl.components.connectionvisual.connectionvisualcomponent import ConnectionVisualObject
    from umlfri2.ufl.components.visual.visualcontainer import VisualObjectContainer


class ConnectionObject:
    def __init__(self, type: ConnectionType, source: ElementObject, destination: ElementObject,
                 save_id: Optional[UUID] = None) -> None:
        self.__type = type
        self.__data = type.ufl_type.build_default(None)
        self.__source = ref(source)
        self.__destination = ref(destination)
        self.__visuals = WeakSet()
        self.__cache = ModelTemporaryDataCache(None)
        if save_id is None:
            self.__save_id = uuid4()
        else:
            self.__save_id = save_id
    
    def add_visual(self, visual: ConnectionVisual) -> None:
        if visual.object is not self:
            raise Exception
        self.__visuals.add(visual)
    
    def remove_visual(self, visual: ConnectionVisual) -> None:
        self.__visuals.remove(visual)
    
    @property
    def visuals(self) -> Iterator[ConnectionVisual]:
        yield from self.__visuals
    
    @property
    def cache(self) -> ModelTemporaryDataCache:
        return self.__cache
    
    @property
    def type(self) -> ConnectionType:
        return self.__type
    
    @property
    def data(self) -> UflObject:
        return self.__data
    
    @property
    def source(self) -> ElementObject:
        return self.__source()
    
    @property
    def destination(self) -> ElementObject:
        return self.__destination()
    
    @property
    def project(self) -> Project:
        return self.__source().project
    
    def reverse(self) -> None:
        self.__source, self.__destination = self.__destination, self.__source
        for visual in self.__visuals:
            visual._reverse()
        self.__cache.invalidate()
    
    def get_other_end(self, element: ElementObject) -> Optional[ElementObject]:
        if self.__source() is element:
            return self.__destination()
        elif self.__destination() is element:
            return self.__source()
        else:
            return None
    
    def is_connected_with(self, element: ElementObject) -> bool:
        return self.__source() is element or self.__destination() is element
    
    @property
    def save_id(self) -> UUID:
        return self.__save_id
    
    def create_appearance_object(self, ruler: Ruler) -> ConnectionVisualObject:
        return self.__type.create_appearance_object(self, ruler)
    
    def create_label_object(self, id: str, ruler: Ruler) -> VisualObjectContainer:
        return self.__type.get_label(id).create_appearance_object(self, ruler)
    
    def apply_ufl_patch(self, patch: UflObjectPatch) -> None:
        self.__data.apply_patch(patch)
        self.__cache.refresh()
    
    @property
    def has_ufl_dialog(self) -> bool:
        return self.__type.ufl_type.has_attributes
    
    def create_ufl_dialog(self, options: UflDialogOptions = UflDialogOptions.standard) -> UflDialog:
        if not self.__type.ufl_type.has_attributes:
            raise Exception
        dialog = UflDialog(self.__type.ufl_type, options)
        dialog.associate(self.__data)
        return dialog
