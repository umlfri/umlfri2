from .tabs import *
from .columns import *
from .widgets import *
from ..objects.mutable import UflMutable as UflMutable
from ..types.basic import UflBoolType as UflBoolType, UflDecimalType as UflDecimalType, UflIntegerType as UflIntegerType, UflStringType as UflStringType
from ..types.complex import UflColorType as UflColorType, UflFontType as UflFontType
from ..types.enum import UflEnumType as UflEnumType, UflFlagsType as UflFlagsType
from ..types.structured import UflListType as UflListType, UflNullableType as UflNullableType, UflObjectType as UflObjectType
from .options import UflDialogOptions as UflDialogOptions
from _typeshed import Incomplete
from collections.abc import Generator

from typing import (
    Iterator,
    Optional,
    Union,
)
from umlfri2.metamodel.translation.translation import Translation
from umlfri2.ufl.dialog.options import UflDialogOptions
from umlfri2.ufl.dialog.tabs.listtab import UflDialogListTab
from umlfri2.ufl.dialog.tabs.objecttab import UflDialogObjectTab
from umlfri2.ufl.dialog.tabs.valuetab import UflDialogValueTab
from umlfri2.ufl.objects.immutable.object import UflObject
from umlfri2.ufl.objects.mutable.list import UflMutableList
from umlfri2.ufl.objects.mutable.object import UflMutableObject
from umlfri2.ufl.objects.patch.object import UflObjectPatch
from umlfri2.ufl.types.structured.list import UflListType
from umlfri2.ufl.types.structured.object import UflObjectType

class UflDialog:
    def __init__(
        self,
        type: Union[UflObjectType, UflListType],
        options: UflDialogOptions = ...
    ) -> None: ...
    @property
    def should_save_tab(self) -> bool: ...
    @property
    def has_changes(self): ...
    def switch_tab(self, index: int) -> None: ...
    @property
    def current_tab(self) -> UflDialogListTab: ...
    @property
    def original_object(self): ...
    def finish(self) -> None: ...
    def make_patch(self) -> UflObjectPatch: ...
    @property
    def tabs(
        self
    ) -> Iterator[Union[UflDialogObjectTab, UflDialogListTab, UflDialogValueTab]]: ...
    def get_lonely_tab(
        self
    ) -> Optional[Union[UflDialogListTab, UflDialogObjectTab]]: ...
    def associate(
        self,
        ufl_object: Optional[Union[UflMutableList, UflMutableObject, UflObject]]
    ) -> None: ...
    def refresh(self) -> None: ...
    def translate(self, translation: Translation) -> None: ...
    def reset(self) -> None: ...
