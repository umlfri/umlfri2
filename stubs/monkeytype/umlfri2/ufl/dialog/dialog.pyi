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
    def associate(
        self,
        ufl_object: Optional[Union[UflMutableList, UflMutableObject, UflObject]]
    ) -> None: ...
    @property
    def current_tab(self) -> UflDialogListTab: ...
    def finish(self) -> None: ...
    def get_lonely_tab(
        self
    ) -> Optional[Union[UflDialogListTab, UflDialogObjectTab]]: ...
    def make_patch(self) -> UflObjectPatch: ...
    def refresh(self) -> None: ...
    def reset(self) -> None: ...
    @property
    def should_save_tab(self) -> bool: ...
    def switch_tab(self, index: int) -> None: ...
    @property
    def tabs(
        self
    ) -> Iterator[Union[UflDialogObjectTab, UflDialogListTab, UflDialogValueTab]]: ...
    def translate(self, translation: Translation) -> None: ...
