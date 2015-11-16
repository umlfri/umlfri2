from .widget import UflDialogWidget


class UflDialogChildWidget(UflDialogWidget):
    def __init__(self, tab, id, dialog): 
        super().__init__(tab, id)
        self.__dialog = dialog
    
    @property
    def dialog(self):
        return self.__dialog
