from .interface import Interface


class IConnectionLabel(Interface):
    def __init__(self, executor):
        self.__executor = executor

    @property
    def id(self):
        raise NotImplementedError

    @property
    def api_name(self):
        return 'ConnectionLabel'

    def get_center(self):
        raise NotImplementedError

    def get_connection(self):
        raise NotImplementedError

    def get_diagram(self):
        raise NotImplementedError

    def get_position(self):
        raise NotImplementedError

    def get_size(self):
        raise NotImplementedError
