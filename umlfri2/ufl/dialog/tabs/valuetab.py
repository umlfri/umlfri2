from ..widgets import UflDialogValuedWidget, UflDialogChildWidget
from .tab import UflDialogTab


class UflDialogValueTab(UflDialogTab):
    def associate(self, ufl_object):
        self._set_current_object(ufl_object)
    
    def add_widget(self, widget):
        if widget.id is not None:
            raise Exception("Only unidentified widget can be added to a value tab")
        for widget in self.widgets:
            raise Exception("There already is a widget on this tab")
        super().add_widget(widget)
    
    def finish(self):
        for widget in self.widgets:
            if isinstance(widget, UflDialogValuedWidget):
                self._set_current_object(widget.value)
            elif isinstance(widget, UflDialogChildWidget):
                widget.dialog.finish()
