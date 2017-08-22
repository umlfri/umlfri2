from .column import UflDialogColumn


class UflDialogValuedColumn(UflDialogColumn):
    def get_value(self, object):
        return str(self._get_real_value(object))
