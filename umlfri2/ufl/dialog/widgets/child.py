from .widget import UflDialogWidget


class UflDialogChildWidget(UflDialogWidget):
    def __init__(self, tab, attr, dialog): 
        super().__init__(tab, attr)
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
    
    def translate(self, translation):
        super().translate(translation)
        
        self.__dialog.translate(translation)
