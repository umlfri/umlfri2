from ..diagramtype import DiagramType
from ..elementtype import ElementType
from ..connectiontype import ConnectionType
from ..projecttemplate import ProjectTemplate

from umlfri2.ufl.types import UflObjectAttribute, UflEnumPossibility

from .attributetranslation import AttributeTranslation


class Translation:
    def __init__(self, language, translations):
        self.__language = language
        self.__element_names = {}
        self.__diagram_names = {}
        self.__connection_names = {}
        self.__attribute_names = AttributeTranslation()
        self.__enum_item_names = AttributeTranslation()
        self.__template_names = {}
        
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
            elif type == 'enumitem':
                if path.endswith('*'):
                    raise Exception
                child = self.__enum_item_names
                for part in reversed(path.split('/')):
                    child = child.add_parent(part)
                child.label = label
            elif type == 'template':
                self.__template_names[path] = label
    
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
            ret = self.__attribute_names.translate(object)
            if ret is None:
                return object.name
            else:
                return ret
        elif isinstance(object, UflEnumPossibility):
            ret = self.__enum_item_names.translate(object)
            if ret is None:
                return object.name
            else:
                return ret
        elif isinstance(object, ProjectTemplate):
            return self.__template_names.get(object.id, object.id)
        raise Exception


POSIX_TRANSLATION = Translation("POSIX", ())
