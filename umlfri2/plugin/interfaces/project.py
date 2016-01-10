from .interface import Interface


class IProject(Interface):
    def __init__(self, executor, project):
        super().__init__(executor)
        self.__project = project

    @property
    def id(self):
        return str(self.__project.save_id)

    @property
    def api_name(self):
        return 'Project'

    def get_children(self):
        raise NotImplementedError

    def get_metamodel(self):
        raise NotImplementedError
