from .interface import Interface
from .partnotfound import PartNotFound


class IMetamodel(Interface):
    def __init__(self, executor, metamodel):
        super().__init__(executor)
        self.__metamodel = self._ref(metamodel)

    @property
    def id(self):
        return '{{{0}}}metamodel'.format(self.__metamodel().addon.identifier)

    @property
    def api_name(self):
        return 'Metamodel'

    def get_connection(self, name: str):
        from .connectiontype import IConnectionType
        
        try:
            type = self.__metamodel().get_connection_type(name)
        except KeyError as e:
            raise PartNotFound(name) from e
        
        return IConnectionType(self._executor, type)

    def get_connections(self):
        from .connectiontype import IConnectionType
        
        for type in self.__metamodel().connection_types:
            yield IConnectionType(self._executor, type)

    def get_diagram(self, name: str):
        from .diagramtype import IDiagramType
        
        try:
            type = self.__metamodel().get_diagram_type(name)
        except KeyError as e:
            raise PartNotFound(name) from e
        
        return IDiagramType(self._executor, type)

    def get_diagrams(self):
        from .diagramtype import IDiagramType
        
        for type in self.__metamodel().diagram_types:
            yield IDiagramType(self._executor, type)

    def get_element(self, name: str):
        from .elementtype import IElementType
        
        try:
            type = self.__metamodel().get_element_type(name)
        except KeyError as e:
            raise PartNotFound(name) from e
        
        return IElementType(self._executor, type)

    def get_elements(self):
        from .elementtype import IElementType
        
        for type in self.__metamodel().element_types:
            yield IElementType(self._executor, type)

    def get_identifier(self):
        return self.__metamodel().addon.identifier

    def get_version(self):
        return str(self.__metamodel().addon.version)
