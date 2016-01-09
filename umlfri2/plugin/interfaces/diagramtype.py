from .interface import Interface


class IDiagramType(Interface):
    def __init__(self, executor):
        super().__init__(executor)

    @property
    def id(self):
        raise NotImplementedError

    @property
    def api_name(self):
        return 'DiagramType'

    def get_connections(self):
        raise NotImplementedError

    def get_elements(self):
        raise NotImplementedError

    def get_name(self):
        raise NotImplementedError
