from .interface import Interface


class IDiagramType(Interface):
    def __init__(self, executor, diagram):
        super().__init__(executor)
        self.__diagram = diagram

    @property
    def id(self):
        return '{{{0}}}diagram:{1}'.format(self.__diagram.metamodel.addon.identifier, self.__diagram.id)

    @property
    def api_name(self):
        return 'DiagramType'

    def get_connections(self):
        from .connectiontype import IConnectionType
        
        for type in self.__diagram.connection_types:
            yield IConnectionType(self._executor, type)

    def get_elements(self):
        from .elementtype import IElementType
        
        for type in self.__diagram.element_types:
            yield IElementType(self._executor, type)

    def get_name(self):
        return self.__diagram.id
