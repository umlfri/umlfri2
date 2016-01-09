from .interface import Interface


class ISolution(Interface):
    def __init__(self, executor):
        super().__init__(executor)

    @property
    def id(self):
        raise NotImplementedError

    @property
    def api_name(self):
        return 'Solution'

    def get_children(self):
        raise NotImplementedError
