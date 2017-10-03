from .project import Project


class ProjectBuilder:
    def __init__(self, template, name="Project"):
        self.__template = template
        self.__name = name
        self.__project = None
    
    @property
    def project(self):
        if self.__project is None:
            self.__build_project()
        return self.__project

    def __build_project(self):
        self.__project = Project(self.__template.metamodel, name=self.__name)
