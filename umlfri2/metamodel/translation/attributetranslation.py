from umlfri2.ufl.types.structured import UflObjectAttribute, UflObjectType, UflListType
from umlfri2.ufl.types.enum import UflEnumType, UflEnumPossibility, UflFlagsType


class AttributeTranslation:
    def __init__(self, multi=False):
        self.__parents = {}
        self.__multi = multi
        self.__label = None
    
    def add_parent(self, name):
        if name not in self.__parents:
            self.__parents[name] = self.__class__(name == '**')
        return self.__parents[name]
    
    @property
    def label(self):
        return self.__label
    
    @label.setter
    def label(self, value):
        self.__label = value
    
    @property
    def has_parents(self):
        return bool(self.__parents)
    
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
            ret = self.translate(object.parent)
            return ret
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
