from .valued import UflDialogValuedWidget


class UflDialogSelectWidget(UflDialogValuedWidget):
    def __init__(self, tab, id, label, enum): 
        super().__init__(tab, id, label)
        self.__enum = enum
    
    @property
    def possibilities(self):
        for possibility in self.__enum.possibilities:
            yield possibility.name
    
    def get_value(self, name):
        return self.__enum.parse(name)
