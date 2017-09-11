from umlfri2.ufl.types import UflObjectAttribute, UflObjectType, UflListType, UflEnumType, UflEnumPossibility, \
    UflFlagsType


class AttributeTranslation:
    def __init__(self, multi=False):
        self.__parents = {}
        self.__multi = multi
        self.__label = None
    
    def add_parent(self, name):
        if name not in self.__parents:
            self.__parents[name] = AttributeTranslation(name == '**')
        return self.__parents[name]
    
    @property
    def label(self):
        return self.__label
    
    @label.setter
    def label(self, value):
        self.__label = value
    
    def translate(self, object):
        if isinstance(object, UflObjectAttribute):
            for id in (object.name, '*', '**'):
                if id in self.__parents:
                    ret = self.__parents[id].translate(object.parent)
                    if ret is not None:
                        return ret
            if self.__multi:
                return self.translate(object.parent)
            else:
                return None
        elif isinstance(object, (UflObjectType, UflListType, UflEnumType, UflFlagsType)):
            return self.translate(object.parent)
        elif isinstance(object, UflEnumPossibility):
            if object.name in self.__parents:
                ret = self.__parents[object.name].translate(object.enum)
            else:
                ret = None
            if ret is not None:
                return ret
        else:
            for id in (object.id, '*', '**'):
                if id in self.__parents:
                    return self.__parents[id].label
            if self.__multi:
                return self.__label
            else:
                return None
