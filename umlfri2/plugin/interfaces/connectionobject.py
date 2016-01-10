from .helpers.uflobject import UflObjectApiHelper
from .interface import Interface


class IConnectionObject(Interface):
    def __init__(self, executor, connection):
        super().__init__(executor)
        self.__connection = connection

    @property
    def id(self):
        return str(self.__connection.save_id)

    @property
    def api_name(self):
        return 'ConnectionObject'
    
    @property
    def connection_object(self):
        return self.__connection

    def get_destination(self):
        from .elementobject import IElementObject
        
        return IElementObject(self._executor, self.__connection.destination)

    def get_connected_object(self, obj: object):
        from .elementobject import IElementObject
        
        element = self.__connection.get_other_end(obj.element_object)
        return IElementObject(self._executor, element)

    def get_source(self):
        from .elementobject import IElementObject
        
        return IElementObject(self._executor, self.__connection.source)

    def get_type(self):
        from .connectiontype import IConnectionType
        
        return IConnectionType(self._executor, self.__connection.type)

    def get_value(self, path: str):
        return UflObjectApiHelper(self.__connection.data)[path]

    def get_values(self):
        yield from UflObjectApiHelper(self.__connection.data)

    def get_visuals(self):
        from .connectionvisual import IConnectionVisual
        
        for visual in self.__connection.visuals:
            yield IConnectionVisual(self._executor, visual)
