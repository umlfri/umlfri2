from .helpers.uflobject import UflObjectApiHelper
from .interface import Interface


class IDiagram(Interface):
    def __init__(self, executor, diagram):
        super().__init__(executor)
        self.__diagram = self._ref(diagram)

    @property
    def id(self):
        return str(self.__diagram().save_id)

    @property
    def api_name(self):
        return 'Diagram'
    
    @property
    def diagram(self):
        return self.__diagram()

    def get_connections(self):
        raise NotImplementedError

    def get_elements(self):
        raise NotImplementedError

    def get_connection(self, obj: object):
        raise NotImplementedError

    def get_element(self, obj: object):
        raise NotImplementedError

    def get_name(self):
        raise NotImplementedError

    def get_parent(self):
        raise NotImplementedError

    def get_project(self):
        raise NotImplementedError

    def get_selection(self) -> object:
        raise NotImplementedError

    def get_type(self):
        raise NotImplementedError

    def get_value(self, path: str):
        return UflObjectApiHelper(self.__diagram.data)[path]

    def get_values(self):
        yield from UflObjectApiHelper(self.__diagram.data)
