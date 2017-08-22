class UflDialogColumn:
    def __init__(self, attr):
        self.__attr = attr
        if self.__attr is None:
            self.__title = None
        else:
            self.__title = attr.name
    
    @property
    def title(self):
        return self.__title
    
    def get_value(self, object):
        if self.__attr is None:
            return str(object)
        else:
            return str(object.get_value(self.__attr.name))
    
    def translate(self, translation):
        if self.__attr is not None:
            self.__title = translation.translate(self.__attr)
