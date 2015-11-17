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
    
    def associate(self, ufl_object):
        raise NotImplementedError
