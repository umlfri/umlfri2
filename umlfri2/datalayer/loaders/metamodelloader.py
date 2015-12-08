import lxml.etree

from .templateloader import TemplateLoader
from ..constants import ADDON_NAMESPACE, MODEL_NAMESPACE
from .elementtypeloader import ElementTypeLoader
from .diagramtypeloader import DiagramTypeLoader
from .connectiontypeloader import ConnectionTypeLoader
from .definitionsloader import DefinitionsLoader
from umlfri2.metamodel import Metamodel


class MetamodelLoader:
    def __init__(self, storage, addon_storage, addon_info):
        self.__addon_storage = addon_storage
        self.__storage = storage
        self.__addon_info = addon_info
    
    def load(self):
        elementXMLs = []
        connectionXMLs = []
        diagramXMLs = []
        templateXMLs = []
        definitionXMLs = None # TODO: multiple definition files
        for file in self.__storage.get_all_files():
            xml = lxml.etree.parse(self.__storage.open(file)).getroot()
            if xml.tag == "{{{0}}}ElementType".format(ADDON_NAMESPACE):
                elementXMLs.append((file, xml))
            elif xml.tag == "{{{0}}}ConnectionType".format(ADDON_NAMESPACE):
                connectionXMLs.append((file, xml))
            elif xml.tag == "{{{0}}}DiagramType".format(ADDON_NAMESPACE):
                diagramXMLs.append((file, xml))
            elif xml.tag == "{{{0}}}Definitions".format(ADDON_NAMESPACE):
                definitionXMLs = (file, xml)
            elif xml.tag == "{{{0}}}Project".format(MODEL_NAMESPACE):
                templateXMLs.append((file, xml))
        
        if definitionXMLs is not None:
            definitions = DefinitionsLoader(definitionXMLs[1]).load()
        else:
            definitions = None
        
        connections = {}
        for file, connection in connectionXMLs:
            loaded = ConnectionTypeLoader(self.__addon_storage, connection, definitions).load()
            connections[loaded.id] = loaded
        
        elements = {}
        for file, element in elementXMLs:
            loaded = ElementTypeLoader(self.__addon_storage, element).load()
            elements[loaded.id] = loaded
        
        diagrams = {}
        for file, diagram in diagramXMLs:
            loaded = DiagramTypeLoader(self.__addon_storage, diagram, elements, connections).load()
            diagrams[loaded.id] = loaded
        
        templates = []
        for file, template in templateXMLs:
            templates.append(TemplateLoader(self.__storage, template, file, self.__addon_info.identifier).load())
        
        return Metamodel(diagrams, elements, connections, templates)
