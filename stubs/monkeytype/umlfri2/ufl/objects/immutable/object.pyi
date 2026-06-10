from typing import (
    Any,
    Dict,
)
from umlfri2.ufl.objects.mutable.object import UflMutableObject
from umlfri2.ufl.objects.patch.object import UflObjectPatch
from umlfri2.ufl.types.structured.object import UflObjectType


class UflObject:
    def __init__(self, type: UflObjectType, attributes: Dict[str, Any]) -> None: ...
    def apply_patch(self, patch: UflObjectPatch) -> None: ...
    def get_value(self, name: str) -> Any: ...
    def make_mutable(self) -> UflMutableObject: ...
