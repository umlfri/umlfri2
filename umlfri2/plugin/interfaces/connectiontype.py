from .interface import Interface


class IConnectionType(Interface):
    def __init__(self, executor, connection):
        super().__init__(executor)
        self.__connection = self._ref(connection)

    @property
    def id(self):
        return '{{{0}}}connection:{1}'.format(self.__connection().metamodel.addon.identifier, self.__connection().id)

    @property
    def api_name(self):
        return 'ConnectionType'

    def get_name(self):
        return self.__connection().id
