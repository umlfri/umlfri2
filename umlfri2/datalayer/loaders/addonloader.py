import os
import os.path

import lxml.etree

from .addoninfoloader import AddOnInfoLoader
from umlfri2.addon import AddOn
from .constants import NAMESPACE
from .elementtypeloader import ElementTypeLoader
from .diagramtypeloader import DiagramTypeLoader
from .connectiontypeloader import ConnectionTypeLoader
from .definitionsloader import DefinitionsLoader
from umlfri2.metamodel import Metamodel


class AddOnLoader:
    def __init__(self, storage):
        self.__storage = storage
    
    def load(self):
        info = AddOnInfoLoader(lxml.etree.parse(self.__storage.read('addon.xml')).getroot()).load()
        
        metamodel = None
        if info.metamodel:
            metamodel = self.__load_metamodel(self.__storage.sub_open(info.metamodel))
        
        ret = AddOn(info.identifier, info.name, info.version, info.author, info.homepage,
                     info.license, info.icon, info.description, info.config, None,
                     metamodel)
        
        ret.compile()
        
        return ret
    
    def __load_metamodel(self, storage):
        elementXMLs = []
        connectionXMLs = []
        diagramXMLs = []
        definitionXMLs = None # TODO: multiple definition files
        for file in storage.get_all_files():
            xml = lxml.etree.parse(storage.read(file)).getroot()
            if xml.tag == "{{{0}}}ElementType".format(NAMESPACE):
                elementXMLs.append(xml)
            elif xml.tag == "{{{0}}}ConnectionType".format(NAMESPACE):
                connectionXMLs.append(xml)
            elif xml.tag == "{{{0}}}DiagramType".format(NAMESPACE):
                diagramXMLs.append(xml)
            elif xml.tag == "{{{0}}}Definitions".format(NAMESPACE):
                definitionXMLs = xml
        
        if definitionXMLs is not None:
            definitions = DefinitionsLoader(definitionXMLs).load()
        else:
            definitions = None
        
        connections = {}
        for connection in connectionXMLs:
            loaded = ConnectionTypeLoader(connection, definitions).load()
            connections[loaded.id] = loaded
        
        elements = {}
        for element in elementXMLs:
            loaded = ElementTypeLoader(element).load()
            elements[loaded.id] = loaded
        
        diagrams = {}
        for diagram in diagramXMLs:
            loaded = DiagramTypeLoader(diagram, elements, connections).load()
            diagrams[loaded.id] = loaded
        
        return Metamodel(diagrams, elements, connections)
