from .interface import Interface


class IElementObject(Interface):
    def __init__(self, executor, element):
        super().__init__(executor)
        self.__element = element

    @property
    def id(self):
        return str(self.__element.save_id)

    @property
    def api_name(self):
        return 'ElementObject'

    def get_children(self):
        raise NotImplementedError

    def get_connections(self):
        raise NotImplementedError

    def get_diagrams(self):
        raise NotImplementedError

    def get_name(self):
        raise NotImplementedError

    def get_parent(self):
        raise NotImplementedError

    def get_project(self):
        raise NotImplementedError

    def get_type(self):
        raise NotImplementedError

    def get_value(self, path: str):
        raise NotImplementedError

    def get_values(self):
        raise NotImplementedError

    def get_visuals(self):
        raise NotImplementedError
