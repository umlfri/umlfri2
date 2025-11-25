from __future__ import annotations

from typing import Iterator, Optional, TYPE_CHECKING, Union
from uuid import UUID, uuid4

from umlfri2.model import ElementObject
from umlfri2.ufl.dialog import UflDialog

if TYPE_CHECKING:
    from umlfri2.metamodel import Metamodel
    from umlfri2.metamodel.elementtype import ElementType
    from umlfri2.ufl.objects import UflObject, UflObjectPatch


class Project:
    def __init__(self, metamodel: Metamodel, name: Optional[str] = None, save_id: Optional[UUID] = None) -> None:
        if name is None:
            self.__name = "Project"
        else:
            self.__name = name
        self.__metamodel = metamodel
        self.__children: list = []
        if save_id is None:
            self.__save_id = uuid4()
        else:
            self.__save_id = save_id
        
        self.__config = metamodel.config_structure.build_default(None)

    @property
    def parent(self) -> None:
        return None
    
    def get_display_name(self) -> str:
        return self.__name
    
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, new_name: str) -> None:
        self.__name = new_name
    
    @property
    def metamodel(self) -> Metamodel:
        return self.__metamodel
    
    @property
    def children_count(self) -> int:
        return len(self.__children)
    
    @property
    def children(self) -> Iterator[ElementObject]:
        yield from self.__children
    
    @property
    def save_id(self) -> UUID:
        return self.__save_id
    
    def create_child_element(self, type: ElementType, save_id: Optional[UUID] = None) -> ElementObject:
        obj = ElementObject(self, type, save_id)
        self.__children.append(obj)
        return obj
    
    def get_child_index(self, obj: ElementObject) -> int:
        return self.__children.index(obj)
    
    def add_child(self, obj: ElementObject, index: Optional[int] = None) -> None:
        if obj.parent is not self:
            raise Exception
        if obj in self.__children:
            raise Exception
        
        if index is None:
            self.__children.append(obj)
        else:
            self.__children.insert(index, obj)
    
    def remove_child(self, obj: ElementObject) -> None:
        if obj.parent is not self:
            raise Exception
        if obj not in self.__children:
            raise Exception
        self.__children.remove(obj)
    
    def get_all_elements(self) -> Iterator[ElementObject]:
        def recursion(obj: Union[Project, ElementObject]) -> Iterator[ElementObject]:
            for child in obj.children:
                yield child
                yield from recursion(child)
        
        return recursion(self)
    
    def invalidate_all_caches(self) -> None:
        for element in self.__children:
            element.invalidate_all_caches()
    
    @property
    def config(self) -> UflObject:
        return self.__config
    
    def apply_config_patch(self, patch: UflObjectPatch) -> None:
        if not self.__metamodel.has_config:
            raise Exception
        self.__config.apply_patch(patch)
    
    def create_config_dialog(self) -> UflDialog:
        if not self.__metamodel.has_config:
            raise Exception
        dialog = UflDialog(self.__metamodel.config_structure)
        dialog.associate(self.__config)
        return dialog
