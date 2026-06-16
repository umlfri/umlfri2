from .column import UflDialogColumn as UflDialogColumn

from umlfri2.ufl.objects.mutable.object import UflMutableObject

class UflDialogCheckColumn(UflDialogColumn):
    def get_value(self, object: UflMutableObject) -> str: ...
