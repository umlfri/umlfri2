from typing import (
    Iterator,
    List,
    Optional,
)
from umlfri2.ufl.objects.immutable.object import UflObject
from umlfri2.ufl.objects.mutable.list import UflMutableList
from umlfri2.ufl.objects.patch.list import UflListPatch
from umlfri2.ufl.types.structured.list import UflListType


class UflList:
    def __init__(
        self,
        type: UflListType,
        values: Optional[List[UflObject]] = ...
    ) -> None: ...
    def __iter__(self) -> Iterator[UflObject]: ...
    def apply_patch(self, patch: UflListPatch) -> None: ...
    def get_length(self) -> int: ...
    def make_mutable(self) -> UflMutableList: ...
