from collections import OrderedDict
from weakref import ref
from typing import Dict, Iterable, Optional, TYPE_CHECKING

from umlfri2.ufl.context import TypeContext
from umlfri2.ufl.types.structured import UflObjectType
from .translation import TranslationList

if TYPE_CHECKING:
    from .diagramtype import DiagramType
    from .elementtype import ElementType
    from .connectiontype import ConnectionType
    from .projecttemplate.project import ProjectTemplate
    from .translation.translation import Translation


class Metamodel:
    def __init__(self, diagrams: Dict[str, 'DiagramType'], elements: Dict[str, 'ElementType'], 
                 connections: Dict[str, 'ConnectionType'], templates: Iterable['ProjectTemplate'],
                 definitions, translations: Dict[str, 'Translation'], config: Optional[UflObjectType]) -> None:
        self.__diagrams = OrderedDict(item for item in sorted(diagrams.items()))
        self.__elements = OrderedDict(item for item in sorted(elements.items()))
        self.__connections = OrderedDict(item for item in sorted(connections.items()))
        self.__templates = list(templates)
        self.__templates.sort(key=lambda item: item.id)
        self.__translations = TranslationList(translations)
        
        self.__definitions = definitions
        
        if config is None or not config.has_attributes:
            self.__config_structure = UflObjectType(())
            self.__has_config = False
        else:
            self.__config_structure = config
            self.__has_config = True
        self.__config_structure.set_parent(self)
        
        self.__addon = None
    
    def _set_addon(self, addon):
        self.__addon = ref(addon)
        
        for diagram in self.__diagrams.values():
            diagram._set_metamodel(self)
        
        for element in self.__elements.values():
            element._set_metamodel(self)
        
        for connection in self.__connections.values():
            connection._set_metamodel(self)
        
        for template in self.__templates:
            template._set_metamodel(self)
    
    @property
    def addon(self):
        return self.__addon()
    
    @property
    def diagram_types(self) -> Iterable['DiagramType']:
        yield from self.__diagrams.values()
    
    @property
    def element_types(self) -> Iterable['ElementType']:
        yield from self.__elements.values()
    
    @property
    def connection_types(self) -> Iterable['ConnectionType']:
        yield from self.__connections.values()
    
    @property
    def templates(self) -> Iterable['ProjectTemplate']:
        yield from self.__templates
    
    def get_element_type(self, name: str) -> 'ElementType':
        return self.__elements[name]
    
    def get_diagram_type(self, name: str) -> 'DiagramType':
        return self.__diagrams[name]
    
    def get_connection_type(self, name: str) -> 'ConnectionType':
        return self.__connections[name]

    def get_translation(self, language: str) -> 'Translation':
        return self.__translations.get_translation(language)
    
    @property
    def config_structure(self) -> UflObjectType:
        return self.__config_structure
    
    @property
    def has_config(self) -> bool:
        return self.__has_config
    
    def compile(self) -> None:
        type_context = TypeContext(self.__definitions)
        for diagram in self.__diagrams.values():
            diagram.compile(type_context)
        
        for element in self.__elements.values():
            element.compile(type_context)
        
        for connection in self.__connections.values():
            connection.compile(type_context)
        
        for template in self.__templates:
            template.compile()
