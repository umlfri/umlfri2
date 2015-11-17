from umlfri2.ufl.dialog.widgets.valued import UflDialogValuedWidget
from .tab import UflDialogTab


class UflDialogListTab(UflDialogTab):
    def __init__(self, id, name, list_type): 
        super().__init__(id, name)
        self.__list_type = list_type
        self.__list = None
        self.__current_index = None
        self.__is_new = False
    
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
                    row.append(str(object.get_value(name)))
                yield row
    
    @property
    def can_new(self):
        return True
    
    def new(self):
        self.__current_index = None
        self._set_current_object(self.__list.create_default())
        self.__is_new = True
    
    def save(self):
        for widget in self.widgets:
            if isinstance(widget, UflDialogValuedWidget):
                if widget.id is None:
                    if self.__is_new:
                        self._set_current_object(widget.value)
                    else:
                        self.__list.set_item(self.__current_index, widget.value)
                else:
                    self.current_object.set_value(widget.id, widget.value)
        
        if self.__is_new:
            self.__list.append(self.current_object)
            self.new()
    
    @property
    def can_save(self):
        return self.current_object is not None
    
    @property
    def can_delete(self):
        return self.__current_index is not None
    
    def delete(self):
        self.__list.delete(self.__current_index)
    
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
        
        self.__is_new = False
    
    def associate(self, ufl_object):
        self.__list = ufl_object
        self.current_index = None
