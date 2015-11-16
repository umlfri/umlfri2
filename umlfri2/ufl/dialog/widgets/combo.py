from .widget import UflDialogWidget


class UflDialogComboWidget(UflDialogWidget):
    def __init__(self, tab, id, possibilities): 
        super().__init__(tab, id)
        self.__possibilities = possibilities
    
    @property
    def possibilities(self):
        yield from self.__possibilities
