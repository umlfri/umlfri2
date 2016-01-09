from .interface import Interface


class IElementVisual(Interface):
    def __init__(self, executor):
        self.__executor = executor

    @property
    def id(self):
        raise NotImplementedError

    @property
    def api_name(self):
        return 'ElementVisual'

    def get_center(self):
        raise NotImplementedError

    def get_connections(self):
        raise NotImplementedError

    def get_diagram(self):
        raise NotImplementedError

    def get_minimal_size(self):
        raise NotImplementedError

    def get_object(self):
        raise NotImplementedError

    def get_position(self):
        raise NotImplementedError

    def get_size(self):
        raise NotImplementedError
