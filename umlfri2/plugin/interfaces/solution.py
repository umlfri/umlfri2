from .interface import Interface


class ISolution(Interface):
    def __init__(self, executor):
        self.__executor = executor

    @property
    def id(self):
        raise NotImplementedError

    @property
    def api_name(self):
        return 'Solution'

    def get_children(self):
        raise NotImplementedError
