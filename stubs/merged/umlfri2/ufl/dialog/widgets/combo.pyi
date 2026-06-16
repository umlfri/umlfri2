from .valued import UflDialogValuedWidget as UflDialogValuedWidget
from _typeshed import Incomplete
from collections.abc import Generator

from typing import Iterator
from umlfri2.ufl.dialog.tabs.objecttab import UflDialogObjectTab
from umlfri2.ufl.types.basic.string import UflStringType
from umlfri2.ufl.types.structured.object import UflObjectAttribute

class UflDialogComboWidget(UflDialogValuedWidget):
    def __init__(
        self,
        tab: UflDialogObjectTab,
        attr: UflObjectAttribute,
        type: UflStringType
    ) -> None: ...
    @property
    def possibilities(self) -> Iterator[str]: ...
