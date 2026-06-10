from typing import (
    Optional,
    Union,
)
from umlfri2.metamodel.translation.translation import Translation
from umlfri2.ufl.dialog.tabs.listtab import UflDialogListTab
from umlfri2.ufl.dialog.tabs.objecttab import UflDialogObjectTab
from umlfri2.ufl.dialog.tabs.valuetab import UflDialogValueTab
from umlfri2.ufl.types.base.type import UflType
from umlfri2.ufl.types.enum.stringenum import UflStringEnumType
from umlfri2.ufl.types.structured.object import UflObjectAttribute


class UflDialogWidget:
    def __init__(
        self,
        tab: Union[UflDialogValueTab, UflDialogObjectTab, UflDialogListTab],
        attr: Optional[UflObjectAttribute],
        type: UflType
    ) -> None: ...
    @property
    def id(self) -> Optional[str]: ...
    @property
    def label(self) -> str: ...
    def translate(self, translation: Translation) -> None: ...
    @property
    def type(self) -> UflStringEnumType: ...
