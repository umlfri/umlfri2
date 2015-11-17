from weakref import ref


class UflDialogWidget:
    def __init__(self, tab, id, label):
        self.__tab = ref(tab)
        self.__id = id
        self.__label = label
    
    @property
    def id(self):
        return self.__id
    
    @property
    def label(self):
        return self.__label
    
    @property
    def value(self):
        return self.__tab().get_value(self.__id)
