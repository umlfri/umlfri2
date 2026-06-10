from typing import (
    Optional,
    Union,
)
from umlfri2.ufl.dialog.tabs.listtab import UflDialogListTab
from umlfri2.ufl.dialog.tabs.objecttab import UflDialogObjectTab
from umlfri2.ufl.dialog.tabs.valuetab import UflDialogValueTab
from umlfri2.ufl.objects.mutable.object import UflMutableObject
from umlfri2.ufl.types.basic.bool import UflBoolType
from umlfri2.ufl.types.basic.string import UflStringType
from umlfri2.ufl.types.complex.color import UflColorType
from umlfri2.ufl.types.complex.font import UflFontType
from umlfri2.ufl.types.enum.stringenum import UflStringEnumType
from umlfri2.ufl.types.structured.object import UflObjectAttribute


class UflDialogValuedWidget:
    def __init__(
        self,
        tab: Union[UflDialogValueTab, UflDialogListTab, UflDialogObjectTab],
        attr: Optional[UflObjectAttribute],
        type: Union[UflStringType, UflStringEnumType, UflFontType, UflBoolType, UflColorType]
    ) -> None: ...
    def associate(self, ufl_object: Optional[Union[UflMutableObject, str]]) -> None: ...
    @property
    def changed(self) -> bool: ...
    def finish_after_save(self) -> None: ...
