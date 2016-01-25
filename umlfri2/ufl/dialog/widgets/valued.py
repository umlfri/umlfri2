from .widget import UflDialogWidget


class UflDialogValuedWidget(UflDialogWidget):
    def __init__(self, tab, attr): 
        super().__init__(tab, attr)
        self.__value = None
        self.__old_value = None
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        self.__value = value
    
    def associate(self, ufl_object):
        if ufl_object is None:
            self.__value = None
        elif self.id is None:
            self.__value = ufl_object
        else:
            self.__value = ufl_object.get_value(self.id)
        self.__old_value = self.__value
    
    @property
    def changed(self):
        return self.__value != self.__old_value
    
    def finish_after_save(self):
        self.__old_value = self.__value
    
    def discard(self):
        self.__value = self.__old_value
