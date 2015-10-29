import lxml.etree
import os
import os.path

from .addoninfoloader import AddOnInfoLoader
from ..addon import AddOn
from .constants import NAMESPACE
from .elementtypeloader import ElementTypeLoader
from .diagramtypeloader import DiagramTypeLoader
from .connectiontypeloader import ConnectionTypeLoader
from umlfri2.metamodel import Metamodel


class AddOnLoader:
    def __init__(self, path):
        self.__path = path
    
    def load(self):
        info = AddOnInfoLoader(lxml.etree.parse(open(os.path.join(self.__path, 'addon.xml'))).getroot()).load()
        
        metamodel = None
        if info.metamodel:
            metamodel = self.__load_metamodel(os.path.join(self.__path, info.metamodel))
        
        ret = AddOn(info.identifier, info.name, info.version, info.author, info.homepage,
                     info.license, info.icon, info.description, info.config, None,
                     metamodel)
        
        ret.compile()
        
        return ret
    
    def __load_metamodel(self, path):
        elementXMLs = []
        connectionXMLs = []
        diagramXMLs = []
        for dirpath, dirs, files in os.walk(path):
            for file in files:
                file = os.path.join(dirpath, file)
                xml = lxml.etree.parse(open(file)).getroot()
                if xml.tag == "{{{0}}}ElementType".format(NAMESPACE):
                    elementXMLs.append(xml)
                elif xml.tag == "{{{0}}}ConnectionType".format(NAMESPACE):
                    connectionXMLs.append(xml)
                elif xml.tag == "{{{0}}}DiagramType".format(NAMESPACE):
                    diagramXMLs.append(xml)
        
        connections = {}
        for connection in connectionXMLs:
            loaded = ConnectionTypeLoader(connection).load()
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
