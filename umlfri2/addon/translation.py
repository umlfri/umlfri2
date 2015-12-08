from umlfri2.metamodel import DiagramType, ElementType, ConnectionType


class Translation:
    def __init__(self, language, translations):
        self.__language = language
        self.__element_names = {}
        self.__diagram_names = {}
        self.__connection_names = {}
        self.__attribute_names = []
        
        for type, path, label in translations:
            if type == 'element':
                self.__element_names[path] = label
            elif type == 'diagram':
                self.__diagram_names[path] = label
            elif type == 'connection':
                self.__connection_names[path] = label
    
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


POSIX_TRANSLATION = Translation("POSIX", ())
