from .column import UflDialogColumn


class UflDialogCheckColumn(UflDialogColumn):
    def get_value(self, object):
        if self._get_real_value(object):
            return "✔"
        else:
            return "✘"
