from .widget import UflDialogWidget


class UflDialogChildWidget(UflDialogWidget):
    def __init__(self, tab, id, label, dialog): 
        super().__init__(tab, id, label)
        self.__dialog = dialog
    
    @property
    def dialog(self):
        return self.__dialog
