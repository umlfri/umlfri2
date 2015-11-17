from .tab import UflDialogTab


class UflDialogListTab(UflDialogTab):
    def __init__(self, id, name, list_type): 
        super().__init__(id, name)
        self.__list_type = list_type
        self.__list = None
        self.__current_index = None
    
    @property
    def columns(self):
        if self.__list_type.item_type.is_immutable:
            yield 'Value'
        else:
            for name, type in self.__list_type.item_type.attributes:
                yield name
    
    @property
    def rows(self):
        if self.__list_type.item_type.is_immutable:
            for value in self.__list:
                yield [str(value)]
        else:
            for object in self.__list:
                row = []
                for name, type in self.__list_type.item_type.attributes:
                    row.append(object.get_value(name))
                yield row
    
    @property
    def current_index(self):
        return self.__current_index
    
    @current_index.setter
    def current_index(self, value):
        self.__current_index = value
        
        if value is None:
            self._set_current_object(None)
        else:
            self._set_current_object(self.__list.get_item(value))
    
    def associate(self, ufl_object):
        self.__list = ufl_object
        self._set_current_object(None)
