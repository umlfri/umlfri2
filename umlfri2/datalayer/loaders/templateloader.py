from umlfri2.metamodel.projecttemplate import ProjectTemplate, ElementTemplate
from ..constants import ADDON_NAMESPACE, ADDON_SCHEMA


class TemplateLoader:
    def __init__(self, xmlroot):
        self.__xmlroot = xmlroot
        if not ADDON_SCHEMA.validate(xmlroot):
            raise Exception("Cannot load project: {0}".format(ADDON_SCHEMA.error_log.last_error))
    
    def load(self):
        id = self.__xmlroot.attrib["id"]
        elements = []
        all_objects = {}
        
        for node in self.__xmlroot:
            if node.tag == "{{{0}}}Element".format(ADDON_NAMESPACE):
                elements.append(self.__load_element(node, all_objects))
        
        return ProjectTemplate(id, elements)

    def __load_element(self, node, all_objects):
        type = node.attrib["type"]
        id = node.attrib.get("id")
        
        children = []

        for child in node:
            if child.tag == "{{{0}}}Element".format(ADDON_NAMESPACE):
                children.append(self.__load_element(child, all_objects))

        return self.__register_object(ElementTemplate(type, {}, children, id), all_objects)

    def __register_object(self, object, all_objects):
        if object.id is not None:
            all_objects[object.id] = object
        return object
