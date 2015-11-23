from umlfri2.metamodel.projecttemplate import ProjectTemplate
from umlfri2.types.geometry import Point, Size
from umlfri2.ufl.types import UflObjectType, UflListType
from ..constants import MODEL_NAMESPACE, MODEL_SCHEMA
from umlfri2.model import Project


class TemplateLoader:
    def __init__(self, storage, xmlroot, path, metamodel_identifier):
        self.__xmlroot = xmlroot
        if not MODEL_SCHEMA.validate(xmlroot):
            raise Exception("Cannot load project: {0}".format(MODEL_SCHEMA.error_log.last_error))
        
        self.__storage = storage
        self.__path = path
        self.__metamodel_identifier = metamodel_identifier
    
    def load(self):
        project = None
        
        for node in self.__xmlroot:
            if node.tag == "{{{0}}}Info".format(MODEL_NAMESPACE):
                return self.__load_info(node)
        
        raise Exception

    def __load_info(self, node):
        metamodel = None
        name = None
        
        for child in node:
            if child.tag == "{{{0}}}Name".format(MODEL_NAMESPACE):
                name = child.attrib["name"]
            elif child.tag == "{{{0}}}Metamodel".format(MODEL_NAMESPACE):
                metamodel = child.attrib["id"]
            else:
                raise Exception
        
        if metamodel != self.__metamodel_identifier:
            raise Exception
        
        return ProjectTemplate(self.__storage, name, self.__path)
