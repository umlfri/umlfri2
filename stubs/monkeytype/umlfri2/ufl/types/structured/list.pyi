from typing import Union
from umlfri2.model.element.elementobject import ElementValueGenerator
from umlfri2.ufl.objects.immutable.list import UflList
from umlfri2.ufl.objects.mutable.list import ListItemValueGenerator
from umlfri2.ufl.types.structured.object import (
    UflObjectAttribute,
    UflObjectType,
)


class UflListType:
    def __init__(self, item_type: UflObjectType) -> None: ...
    def build_default(
        self,
        generator: Union[ListItemValueGenerator, ElementValueGenerator]
    ) -> UflList: ...
    def is_default_value(self, value: UflList) -> bool: ...
    @property
    def is_immutable(self) -> bool: ...
    @property
    def item_type(self) -> UflObjectType: ...
    def set_parent(self, parent: UflObjectAttribute) -> None: ...
