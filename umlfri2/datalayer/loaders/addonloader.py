from collections import namedtuple

import lxml.etree

from .templateloader import TemplateLoader
from umlfri2.types.image import Image
from .addoninfoloader import AddOnInfoLoader
from umlfri2.addon import AddOn
from ..constants import ADDON_NAMESPACE, MODEL_NAMESPACE
from .elementtypeloader import ElementTypeLoader
from .diagramtypeloader import DiagramTypeLoader
from .connectiontypeloader import ConnectionTypeLoader
from .definitionsloader import DefinitionsLoader
from umlfri2.metamodel import Metamodel


class AddOnLoader:
    def __init__(self, storage):
        self.__storage = storage
    
    def load(self):
        info = AddOnInfoLoader(lxml.etree.parse(self.__storage.open('addon.xml')).getroot()).load()
        
        metamodel = None
        if info.metamodel:
            metamodel = self.__load_metamodel(info, self.__storage.create_substorage(info.metamodel))
        
        if not self.__storage.exists(info.icon):
            raise Exception("Unknown icon {0}".format(info.icon))
        icon = Image(self.__storage, info.icon)

        
        ret = AddOn(info.identifier, info.name, info.version, info.author, info.homepage,
                     info.license, icon, info.description, info.config, None,
                     metamodel)
        
        ret.compile()
        
        return ret
    
    def __load_metamodel(self, info, storage):
        elementXMLs = []
        connectionXMLs = []
        diagramXMLs = []
        templateXMLs = []
        definitionXMLs = None # TODO: multiple definition files
        for file in storage.get_all_files():
            xml = lxml.etree.parse(storage.open(file)).getroot()
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
            loaded = ConnectionTypeLoader(self.__storage, connection, definitions).load()
            connections[loaded.id] = loaded
        
        elements = {}
        for file, element in elementXMLs:
            loaded = ElementTypeLoader(self.__storage, element).load()
            elements[loaded.id] = loaded
        
        diagrams = {}
        for file, diagram in diagramXMLs:
            loaded = DiagramTypeLoader(self.__storage, diagram, elements, connections).load()
            diagrams[loaded.id] = loaded
        
        templates = []
        for file, template in templateXMLs:
            templates.append(TemplateLoader(self.__storage, template, file, info.identifier).load())
        
        return Metamodel(diagrams, elements, connections, templates)
