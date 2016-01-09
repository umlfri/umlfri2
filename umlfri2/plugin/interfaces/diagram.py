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

    def append_item(self, path: str):
        raise NotImplementedError

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

    def remove_item(self, path: str):
        raise NotImplementedError

    def get_selection(self) -> object:
        raise NotImplementedError

    def get_type(self):
        raise NotImplementedError

    def get_value(self, path: str):
        raise NotImplementedError

    def set_value(self, path: str, value: None):
        raise NotImplementedError

    def get_values(self):
        raise NotImplementedError