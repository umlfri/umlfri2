from .widget import UflDialogWidget as UflDialogWidget

from typing import (
    Optional,
    Union,
)
from umlfri2.metamodel.translation.translation import Translation
from umlfri2.ufl.dialog.dialog import UflDialog
from umlfri2.ufl.dialog.tabs.listtab import UflDialogListTab
from umlfri2.ufl.dialog.tabs.objecttab import UflDialogObjectTab
from umlfri2.ufl.objects.mutable.object import UflMutableObject
from umlfri2.ufl.types.structured.list import UflListType
from umlfri2.ufl.types.structured.object import (
    UflObjectAttribute,
    UflObjectType,
)

class UflDialogChildWidget(UflDialogWidget):
    def __init__(
        self,
        tab: Union[UflDialogObjectTab, UflDialogListTab],
        attr: UflObjectAttribute,
        type: Union[UflListType, UflObjectType],
        dialog: UflDialog
    ) -> None: ...
    @property
    def value(self): ...
    @property
    def dialog(self) -> UflDialog: ...
    def associate(self, ufl_object: Optional[UflMutableObject]) -> None: ...
    def associate_default(self) -> None: ...
    def translate(self, translation: Translation) -> None: ...
    @property
    def changed(self): ...
    def finish_after_save(self) -> None: ...
    def discard(self) -> None: ...
