from .interface import Interface


class IProject(Interface):
    def __init__(self, executor, project):
        super().__init__(executor)
        self.__project = self._ref(project)

    @property
    def id(self):
        return str(self.__project().save_id)

    @property
    def api_name(self):
        return 'Project'

    def get_children(self):
        from .elementobject import IElementObject
        
        for child in self.__project().children:
            yield IElementObject(self._executor, child)

    def get_metamodel(self):
        from .metamodel import IMetamodel
        
        return IMetamodel(self._executor, self.__project().metamodel)
