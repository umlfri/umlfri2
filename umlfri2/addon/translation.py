from umlfri2.metamodel import DiagramType, ElementType, ConnectionType
from umlfri2.ufl.types import UflObjectAttribute, UflObjectType, UflListType


class AttributeTranslation:
    def __init__(self):
        self.__parents = {}
        self.__label = None
    
    def add_parent(self, name):
        if name not in self.__parents:
            self.__parents[name] = AttributeTranslation()
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
            return None
        elif isinstance(object, (UflObjectType, UflListType)):
            return self.translate(object.parent)
        else:
            for id in (object.name, '*', '**'):
                if id in self.__parents:
                    return self.__parents[id].label
            return None


class Translation:
    def __init__(self, language, translations):
        self.__language = language
        self.__element_names = {}
        self.__diagram_names = {}
        self.__connection_names = {}
        self.__attribute_names = AttributeTranslation()
        
        for type, path, label in translations:
            if type == 'element':
                self.__element_names[path] = label
            elif type == 'diagram':
                self.__diagram_names[path] = label
            elif type == 'connection':
                self.__connection_names[path] = label
            elif type == 'attribute':
                child = self.__attribute_names
                for part in reversed(path.split('/')):
                    child = child.add_parent(part)
                child.label = label
    
    @property
    def language(self):
        return self.__language
    
    def translate(self, object):
        if isinstance(object, ConnectionType):
            return self.__connection_names.get(object.id, object.id)
        elif isinstance(object, ElementType):
            return self.__element_names.get(object.id, object.id)
        elif isinstance(object, DiagramType):
            return self.__diagram_names.get(object.id, object.id)
        elif isinstance(object, UflObjectAttribute):
            return self.__attribute_names.translate(object)


POSIX_TRANSLATION = Translation("POSIX", ())
