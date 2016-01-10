from .interface import Interface


class IElementObject(Interface):
    def __init__(self, executor):
        super().__init__(executor)

    @property
    def id(self):
        raise NotImplementedError

    @property
    def api_name(self):
        return 'ElementObject'

    def append_item(self, path: str):
        raise NotImplementedError

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

    def remove_item(self, path: str):
        raise NotImplementedError

    def get_type(self):
        raise NotImplementedError

    def get_value(self, path: str):
        raise NotImplementedError

    def get_values(self):
        raise NotImplementedError

    def get_visuals(self):
        raise NotImplementedError
