from .project import Project
from .element import ElementObject


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
        
        for element in self.__template.elements:
            self.__project.add_child(self.__build_element_object(self.__project, element))

    def __build_element_object(self, parent, element):
        ret = ElementObject(parent, element.type)
        
        for child in element.children:
            ret.add_child(self.__build_element_object(ret, child))
        
        return ret
