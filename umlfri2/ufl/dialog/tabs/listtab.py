from .tab import UflDialogTab


class UflDialogListTab(UflDialogTab):
    def __init__(self, attr, list_type): 
        super().__init__(attr)
        self.__list_type = list_type
        self.__list = None
        self.__current_index = None
        self.__is_new = False
        self.__columns = []
    
    def add_column(self, column):
        self.__columns.append(column)
    
    @property
    def columns(self):
        for column in self.__columns:
            yield column.title
    
    @property
    def rows(self):
        for object in self.__list:
            row = []
            for column in self.__columns:
                row.append(column.get_value(object))
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
            if widget.id is None:
                if self.__is_new:
                    self._set_current_object(widget.value)
                else:
                    self.__list.set_item(self.__current_index, widget.value)
            else:
                self.current_object.set_value(widget.id, widget.value)
            widget.finish_after_save()
        
        if self.__is_new:
            self.__list.append(self.current_object)
            self.new()
    
    def discard(self):
        for widget in self.widgets:
            widget.discard()
    
    @property
    def should_save(self):
        for widget in self.widgets:
            if widget.changed:
                return True
        return False
    
    @property
    def can_save(self):
        return self.current_object is not None
    
    @property
    def can_delete(self):
        return self.__current_index is not None
    
    def delete(self):
        self.__list.delete(self.__current_index)
        self._set_current_object(None)
        self.__current_index = None
    
    @property
    def current_index(self):
        return self.__current_index
    
    def change_current_index(self, value):
        if self.should_save:
            raise Exception
        self.__current_index = value
        
        if value is None:
            self._set_current_object(None)
        else:
            self._set_current_object(self.__list.get_item(value))
        
        self.__is_new = False
    
    def associate(self, ufl_object):
        self.__list = ufl_object
        self.__current_index = None
        self._set_current_object(None)
        self.__is_new = False
    
    def finish(self):
        pass
    
    def translate(self, translation):
        super().translate(translation)

        for column in self.__columns:
            column.translate(translation)
    
    def tab_deselected(self):
        self.__current_index = None
        self._set_current_object(None)
