from .widget import UflDialogWidget


class UflDialogValuedWidget(UflDialogWidget):
    def __init__(self, tab, id, label): 
        super().__init__(tab, id, label)
        self.__value = None
    
    @property
    def value(self):
        return self.__value
    
    def associate(self, ufl_object):
        if ufl_object is None:
            self.__value = None
        elif self.id is None:
            self.__value = ufl_object
        else:
            self.__value = ufl_object.get_value(self.id)
