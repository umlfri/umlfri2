from typing import Union
from umlfri2.ufl.objects.mutable.object import UflMutableObject


class UflDialogObjectTab:
    def associate(self, ufl_object: Union[str, UflMutableObject]) -> None: ...
    def finish(self) -> None: ...
