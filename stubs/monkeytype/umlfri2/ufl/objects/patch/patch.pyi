from typing import (
    Any,
    Iterator,
    List,
    Union,
)
from umlfri2.ufl.objects.patch.list import UflListPatch
from umlfri2.ufl.objects.patch.object import UflObjectPatch
from umlfri2.ufl.types.structured.list import UflListType
from umlfri2.ufl.types.structured.object import UflObjectType


class UflPatch:
    def __init__(
        self,
        type: Union[UflObjectType, UflListType],
        changes: List[Union[UflObjectPatch.AttributeChanged, UflObjectPatch.AttributePatch, Any, UflListPatch.ItemAdded]]
    ) -> None: ...
    def __iter__(
        self
    ) -> Iterator[Union[UflObjectPatch.AttributePatch, UflObjectPatch.AttributeChanged, UflListPatch.ItemAdded]]: ...
    @property
    def has_changes(self) -> bool: ...
    @property
    def type(
        self
    ) -> Union[UflObjectType, UflListType]: ...
