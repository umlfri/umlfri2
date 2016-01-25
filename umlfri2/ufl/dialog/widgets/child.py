from .widget import UflDialogWidget


class UflDialogChildWidget(UflDialogWidget):
    def __init__(self, tab, attr, dialog): 
        super().__init__(tab, attr)
        self.__dialog = dialog
        self.__value = None
        self.__old_value = None
    
    @property
    def value(self):
        return self.__value
    
    @property
    def dialog(self):
        return self.__dialog
    
    def associate(self, ufl_object):
        if ufl_object is None:
            self.__value = None
            self.__old_value = None
        elif self.id is None:
            self.__value = ufl_object
            self.__old_value = self.__value.copy()
        else:
            self.__value = ufl_object.get_value(self.id)
            self.__old_value = self.__value.copy()
        
        self.__dialog.associate(self.__value)
    
    def translate(self, translation):
        super().translate(translation)
        
        self.__dialog.translate(translation)
    
    @property
    def changed(self):
        return self.__value != self.__old_value
    
    def finish_after_save(self):
        self.__dialog.finish()
        self.__old_value = self.__value.copy()
    
    def discard(self):
        self.__value = self.__old_value.copy()
        self.__dialog.associate(self.__value)
