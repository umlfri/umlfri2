class UflDialogWidget:
    def __init__(self, tab, id, label):
        self.__tab = tab
        self.__id = id
        self.__label = label
        self.__value = None
    
    @property
    def label(self):
        return self.__label
