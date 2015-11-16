from .tab import UflDialogTab


class UflDialogListTab(UflDialogTab):
    def __init__(self, name, list_type): 
        super().__init__(name)
        self.__list_type = list_type
    
    @property
    def columns(self):
        if self.__list_type.item_type.is_immutable:
            yield 'Value'
        else:
            for name, type in self.__list_type.item_type.attributes:
                yield name
