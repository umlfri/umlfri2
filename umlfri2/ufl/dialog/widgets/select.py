from .valued import UflDialogValuedWidget


class UflDialogSelectWidget(UflDialogValuedWidget):
    def __init__(self, tab, id, label, items): 
        super().__init__(tab, id, label)
        self.__items = items
    
    @property
    def possibilities(self):
        for label, value in  self.__items:
            yield label
    
    @property
    def current_index(self):
        for index, (label, value) in enumerate(self.__items):
            if value == self.value:
                return index
        return 0
    
    @current_index.setter
    def current_index(self, index):
        self.value = self.__items[index][1]
