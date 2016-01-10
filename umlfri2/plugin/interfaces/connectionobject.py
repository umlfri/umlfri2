from .interface import Interface


class IConnectionObject(Interface):
    def __init__(self, executor):
        super().__init__(executor)

    @property
    def id(self):
        raise NotImplementedError

    @property
    def api_name(self):
        return 'ConnectionObject'

    def get_destination(self):
        raise NotImplementedError

    def get_connected_object(self, obj: object):
        raise NotImplementedError

    def get_source(self):
        raise NotImplementedError

    def get_type(self):
        raise NotImplementedError

    def get_value(self, path: str):
        raise NotImplementedError

    def get_values(self):
        raise NotImplementedError

    def get_visuals(self):
        raise NotImplementedError
