import uuid

from umlfri2.metamodel.projecttemplate import ProjectTemplate, ElementTemplate, DiagramTemplate
from ..constants import ADDON_NAMESPACE, ADDON_SCHEMA


class TemplateLoader:
    def __init__(self, xmlroot):
        self.__last_id = 0
        self.__xmlroot = xmlroot
        if not ADDON_SCHEMA.validate(xmlroot):
            raise Exception("Cannot load project: {0}".format(ADDON_SCHEMA.error_log.last_error))
    
    def load(self):
        id = self.__xmlroot.attrib["id"]
        elements = []
        self.__all_diagrams = []
        self.__provided_ids = set()
        self.__required_ids = set()
        
        for node in self.__xmlroot:
            if node.tag == "{{{0}}}Element".format(ADDON_NAMESPACE):
                elements.append(self.__load_element(node))
        
        if self.__required_ids - self.__provided_ids:
            raise Exception("Missing references in a template")
        
        return ProjectTemplate(id, elements, self.__all_diagrams)
    
    def __load_element(self, node):
        type = node.attrib["type"]
        id = node.attrib.get("id") or self.__new_id()
        
        self.__provide_id(id)
        
        children = []

        for child in node:
            if child.tag == "{{{0}}}Element".format(ADDON_NAMESPACE):
                children.append(self.__load_element(child))
            elif child.tag == "{{{0}}}Diagram".format(ADDON_NAMESPACE):
                self.__all_diagrams.append(self.__load_diagram(child, id))

        return ElementTemplate(type, {}, children, id)
    
    def __load_diagram(self, node, parent_id):
        type = node.attrib["type"]
        
        self.__require_id(parent_id)
        
        return DiagramTemplate(type, parent_id)
    
    def __provide_id(self, id):
        if id in self.__provided_ids:
            raise Exception("Duplicated id in a template: {0}".format(id))
        
        self.__provided_ids.add(id)
    
    def __require_id(self, id):
        self.__required_ids.add(id)

    def __new_id(self):
        self.__last_id += 1
        return self.__last_id
