from .expression import UflExpression


class UflAttributeAccess(UflExpression):
    def __init__(self, obj, attribute):
        self.__object = obj
        self.__attribute = attribute
    
    @property
    def object(self):
        return self.__object
    
    @property
    def attribute(self):
        return self.__attribute
    
    def _get_params(self):
        return self.__object, self.__attribute