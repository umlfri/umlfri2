class UflDialogColumn:
    def __init__(self, attr):
        self.__attr = attr
        self.__title = None
    
    @property
    def title(self):
        return self.__title
    
    def get_value(self, object):
        raise NotImplementedError

    def _get_real_value(self, object):
        if self.__attr is None:
            return object
        else:
            return object.get_value(self.__attr.name)
    
    def translate(self, translation):
        if self.__attr is not None:
            self.__title = translation.translate(self.__attr)
