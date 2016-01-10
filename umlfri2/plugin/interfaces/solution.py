from .interface import Interface


class ISolution(Interface):
    def __init__(self, executor, solution):
        super().__init__(executor)
        self.__solution = self._ref(solution)

    @property
    def id(self):
        return str(self.__solution().save_id)

    @property
    def api_name(self):
        return 'Solution'

    def get_file_name(self):
        return self._application.solution_name

    def get_projects(self):
        from .project import IProject
        
        for project in self.__solution().children:
            yield IProject(self._executor, project)
