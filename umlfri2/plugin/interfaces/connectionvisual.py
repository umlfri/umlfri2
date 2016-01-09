from .interface import Interface


class IConnectionVisual(Interface):
    def __init__(self, executor):
        self.__executor = executor

    @property
    def id(self):
        raise NotImplementedError

    @property
    def api_name(self):
        return 'ConnectionVisual'

    def get_destination(self):
        raise NotImplementedError

    def get_diagram(self):
        raise NotImplementedError

    def get_labels(self):
        raise NotImplementedError

    def get_object(self):
        raise NotImplementedError

    def get_points(self):
        raise NotImplementedError

    def get_source(self):
        raise NotImplementedError
