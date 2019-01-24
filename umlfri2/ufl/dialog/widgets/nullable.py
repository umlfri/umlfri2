from .widget import UflDialogWidget


class UflDialogNullableWidget(UflDialogWidget):
    def __init__(self, tab, attr, inner_widget):
        super().__init__(tab, attr)
        
        self.__is_null = False
        self.__old_is_null = False
        self.__inner_widget = inner_widget
    
    @property
    def inner_widget(self):
        return self.__inner_widget
    
    @property
    def value(self):
        if self.__is_null:
            return None
        else:
            return self.__inner_widget.value
    
    @property
    def is_null(self):
        return self.__is_null
    
    @is_null.setter
    def is_null(self, value):
        self.__is_null = value
    
    def associate(self, ufl_object):
        if ufl_object is None:
            self.__is_null = True
            self.__inner_widget.associate_default()
        elif ufl_object.get_value(self.id) is None:
            self.__is_null = True
            self.__inner_widget.associate_default()
        else:
            self.__is_null = False
            self.__inner_widget.associate(ufl_object)
        self.__old_is_null = self.__is_null
    
    def associate_default(self):
        self.__is_null = True
        self.__old_is_null = True
        self.__inner_widget.associate_default()
    
    @property
    def changed(self):
        return self.__is_null != self.__old_is_null or self.__inner_widget.changed
    
    def finish_after_save(self):
        self.__old_is_null = self.__is_null
        if not self.__is_null:
            self.__inner_widget.finish_after_save()
    
    def discard(self):
        self.__is_null = self.__old_is_null
        if not self.__is_null:
            self.__inner_widget.discard()
