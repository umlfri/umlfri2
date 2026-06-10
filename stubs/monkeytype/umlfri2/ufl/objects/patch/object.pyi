from typing import Union
from umlfri2.types.color import Color
from umlfri2.types.font import Font
from umlfri2.ufl.objects.patch.list import UflListPatch


class UflObjectPatch.AttributeChanged:
    def __init__(
        self,
        name: str,
        old_value: Union[str, Font, Color, bool],
        new_value: Union[str, Font, Color, bool]
    ) -> None: ...
    @property
    def name(self) -> str: ...
    @property
    def new_value(self) -> Union[bool, Font, Color, str]: ...


class UflObjectPatch.AttributePatch:
    def __init__(
        self,
        name: str,
        patch: Union[UflListPatch, UflObjectPatch]
    ) -> None: ...
    @property
    def name(self) -> str: ...
    @property
    def patch(
        self
    ) -> Union[UflListPatch, UflObjectPatch]: ...
