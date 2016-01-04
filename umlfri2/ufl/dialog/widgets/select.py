from .valued import UflDialogValuedWidget


class UflDialogSelectWidget(UflDialogValuedWidget):
    def __init__(self, tab, attr): 
        super().__init__(tab, attr)
        
        self.__items = tuple((None, possibility.value) for possibility in attr.type.possibilities)
    
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
    
    def translate(self, translation):
        super().translate(translation)
        
        self.__items = tuple((translation.translate(possibility), possibility.value)
                             for possibility in self.attribute.type.possibilities)
