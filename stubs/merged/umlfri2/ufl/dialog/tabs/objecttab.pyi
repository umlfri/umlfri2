from ..widgets import UflDialogChildWidget as UflDialogChildWidget, UflDialogNullableWidget as UflDialogNullableWidget, UflDialogValuedWidget as UflDialogValuedWidget
from .tab import UflDialogTab as UflDialogTab

from typing import Union
from umlfri2.ufl.objects.mutable.object import UflMutableObject

class UflDialogObjectTab(UflDialogTab):
    def associate(self, ufl_object: Union[str, UflMutableObject]) -> None: ...
    def finish(self) -> None: ...
