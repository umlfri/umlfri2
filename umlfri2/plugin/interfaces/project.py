from .interface import Interface


class IProject(Interface):
    def __init__(self, executor):
        super().__init__(executor)

    @property
    def id(self):
        raise NotImplementedError

    @property
    def api_name(self):
        return 'Project'

    def get_children(self):
        raise NotImplementedError

    def get_file_name(self):
        raise NotImplementedError

    def get_metamodel(self):
        raise NotImplementedError
