from .widget import UflDialogWidget


class UflDialogChildWidget(UflDialogWidget):
    def __init__(self, tab, id, label, dialog): 
        super().__init__(tab, id, label)
        self.__dialog = dialog
    
    @property
    def dialog(self):
        return self.__dialog
    
    def associate(self, ufl_object):
        if ufl_object is None:
            self.__dialog.associate(None)
        elif self.id is None:
            self.__dialog.associate(ufl_object)
        else:
            self.__dialog.associate(ufl_object.get_value(self.id))

