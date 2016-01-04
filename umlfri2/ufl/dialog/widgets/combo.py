from .valued import UflDialogValuedWidget


class UflDialogComboWidget(UflDialogValuedWidget):
    def __init__(self, tab, attr): 
        super().__init__(tab, attr)
        self.__possibilities = attr.type.possibilities
    
    @property
    def possibilities(self):
        yield from self.__possibilities
