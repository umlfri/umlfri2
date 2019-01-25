from ..widgets import UflDialogValuedWidget, UflDialogChildWidget
from .tab import UflDialogTab


class UflDialogNullableValueTab(UflDialogTab):
    def __init__(self, attr, value_type):
        super().__init__(attr)
        self.__value_type = value_type

    @property
    def is_null(self):
        return self.current_object is None
    
    @is_null.setter
    def is_null(self, value):
        if value:
            if self.current_object is not None:
                self._set_current_object_null()
        else:
            if self.current_object is None:
                self._set_current_object(self.__value_type.inner_type.build_default(None))
    
    def associate(self, ufl_object):
        if ufl_object is None:
            self._set_current_object_null()
        else:
            self._set_current_object(ufl_object)
    
    def add_widget(self, widget):
        if widget.id is not None:
            raise Exception("Only unidentified widget can be added to a value tab")
        for widget in self.widgets:
            raise Exception("There already is a widget on this tab")
        super().add_widget(widget)
    
    @property
    def widget(self):
        for widget in self.widgets:
            return widget
        return None
    
    def finish(self):
        if not self.is_null:
            for widget in self.widgets:
                if isinstance(widget, UflDialogValuedWidget):
                    self._set_current_object(widget.value)
                elif isinstance(widget, UflDialogChildWidget):
                    widget.dialog.finish()
