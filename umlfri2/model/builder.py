from .project import Project
from .element import ElementObject
from .diagram import Diagram


class ProjectBuilder:
    def __init__(self, template, name="Project"):
        self.__template = template
        self.__name = name
        self.__project = None
        self.__all_objects = {}
    
    @property
    def project(self):
        if self.__project is None:
            self.__build_project()
        return self.__project

    def __build_project(self):
        self.__project = Project(self.__template.metamodel, name=self.__name)
        
        for element in self.__template.elements:
            self.__build_element_object(self.__project, element)

        for diagram in self.__template.diagrams:
            self.__build_diagram(diagram)

    def __build_element_object(self, parent, element):
        ret = parent.create_child_element(element.type)
        
        for child in element.children:
            self.__build_element_object(ret, child)
        
        self.__all_objects[element.id] = ret
        
        return ret

    def __build_diagram(self, diagram):
        parent = self.__all_objects[diagram.parent_id]
        diagram = parent.create_child_diagram(diagram.type)
