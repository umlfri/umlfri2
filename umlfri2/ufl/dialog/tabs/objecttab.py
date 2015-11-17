from umlfri2.ufl.dialog.widgets.valued import UflDialogValuedWidget
from .tab import UflDialogTab


class UflDialogObjectTab(UflDialogTab):
    def associate(self, ufl_object):
        self._set_current_object(ufl_object)
    
    def finish(self):
        for widget in self.widgets:
            if isinstance(widget, UflDialogValuedWidget):
                if widget.id is None:
                    self._set_current_object(widget.value)
                else:
                    self.current_object.set_value(widget.id, widget.value)
