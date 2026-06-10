from typing import (
    Iterator,
    Optional,
    Union,
)
from umlfri2.metamodel.translation.translation import Translation
from umlfri2.ufl.dialog.tabs.listtab import UflDialogListTab
from umlfri2.ufl.dialog.tabs.objecttab import UflDialogObjectTab
from umlfri2.ufl.types.enum.stringenum import UflStringEnumType
from umlfri2.ufl.types.structured.object import UflObjectAttribute


class UflDialogSelectWidget:
    def __init__(
        self,
        tab: Union[UflDialogListTab, UflDialogObjectTab],
        attr: UflObjectAttribute,
        type: UflStringEnumType
    ) -> None: ...
    @property
    def possibilities(self) -> Iterator[Optional[str]]: ...
    def translate(self, translation: Translation) -> None: ...
