from .interface import Interface


class IConnectionType(Interface):
    def __init__(self, executor):
        super().__init__(executor)

    @property
    def id(self):
        raise NotImplementedError

    @property
    def api_name(self):
        return 'ConnectionType'

    def get_name(self):
        raise NotImplementedError
