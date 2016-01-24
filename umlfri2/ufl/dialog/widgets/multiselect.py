from .valued import UflDialogValuedWidget


class UflDialogMultiSelectWidget(UflDialogValuedWidget):
    def __init__(self, tab, attr): 
        super().__init__(tab, attr)
        
        self.__items = tuple((None, possibility.value) for possibility in attr.type.possibilities)
    
    @property
    def possibilities(self):
        for label, value in  self.__items:
            yield value in self.value, label
    
    def check(self, index):
        self.value.set(self.__items[index][1])
    
    def uncheck(self, index):
        self.value.unset(self.__items[index][1])
    
    def translate(self, translation):
        super().translate(translation)
        
        self.__items = tuple((translation.translate(possibility), possibility.value)
                             for possibility in self.attribute.type.possibilities)
