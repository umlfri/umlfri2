from .widget import UflDialogWidget


class UflDialogMultiSelectWidget(UflDialogWidget):
    def __init__(self, tab, attr):
        super().__init__(tab, attr)
        
        self.__items = tuple((None, possibility.value) for possibility in attr.type.possibilities)
        
        self.__value = None
        self.__old_value = None
    
    @property
    def value(self):
        return self.__value
    
    def associate(self, ufl_object):
        if ufl_object is None:
            self.__value = None
        elif self.id is None:
            self.__value = ufl_object
        else:
            self.__value = ufl_object.get_value(self.id)
        self.__old_value = self.__value.copy()
    
    def associate_default(self):
        self.__value = self.attribute.type.build_default(None)
        self.__old_value = self.__value
    
    @property
    def changed(self):
        return self.__value != self.__old_value
    
    def finish_after_save(self):
        self.__old_value = self.__value.copy()
    
    def discard(self):
        self.__value = self.__old_value.copy()
    
    @property
    def possibilities(self):
        for label, value in  self.__items:
            yield value in self.value, label
    
    def check(self, index):
        self.__value.set(self.__items[index][1])
    
    def uncheck(self, index):
        self.__value.unset(self.__items[index][1])
    
    def translate(self, translation):
        super().translate(translation)
        
        self.__items = tuple((translation.translate(possibility), possibility.value)
                             for possibility in self.attribute.type.possibilities)
