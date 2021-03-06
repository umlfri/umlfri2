import lxml.etree

from .templateloader import TemplateLoader
from ....constants import ADDON_NAMESPACE
from .elementtypeloader import ElementTypeLoader
from .diagramtypeloader import DiagramTypeLoader
from .connectiontypeloader import ConnectionTypeLoader
from .definitionsloader import DefinitionsLoader
from .translationloader import TranslationLoader
from .structureloader import UflStructureLoader
from umlfri2.metamodel import Metamodel


class MetamodelLoader:
    def __init__(self, storage, addon_storage, addon_info):
        self.__addon_storage = addon_storage
        self.__storage = storage
        self.__addon_info = addon_info
    
    def load(self):
        parser = lxml.etree.XMLParser(remove_comments=True)
        
        elementXMLs = []
        connectionXMLs = []
        diagramXMLs = []
        templateXMLs = []
        definitionXMLs = []
        configXMLs = None
        translationXMLs = []
        for file in self.__storage.get_all_files():
            xml = lxml.etree.parse(self.__storage.open(file), parser=parser).getroot()
            if xml.tag == "{{{0}}}ElementType".format(ADDON_NAMESPACE):
                elementXMLs.append((file, xml))
            elif xml.tag == "{{{0}}}ConnectionType".format(ADDON_NAMESPACE):
                connectionXMLs.append((file, xml))
            elif xml.tag == "{{{0}}}DiagramType".format(ADDON_NAMESPACE):
                diagramXMLs.append((file, xml))
            elif xml.tag == "{{{0}}}Definitions".format(ADDON_NAMESPACE):
                definitionXMLs.append((file, xml))
            elif xml.tag == "{{{0}}}Translation".format(ADDON_NAMESPACE):
                translationXMLs.append((file, xml))
            elif xml.tag == "{{{0}}}Config".format(ADDON_NAMESPACE):
                configXMLs = (file, xml)
            elif xml.tag == "{{{0}}}Template".format(ADDON_NAMESPACE):
                templateXMLs.append((file, xml))
        
        if definitionXMLs is not None:
            definitions = {}
            for file, definition in definitionXMLs:
                for def_name, def_dict in DefinitionsLoader(definition).load().items():
                    definitions.setdefault(def_name, {}).update(def_dict)
        else:
            definitions = {}

        if configXMLs is not None:
            config = UflStructureLoader(configXMLs[1], configXMLs[0]).load()
        else:
            config = None
        
        connections = {}
        for file, connection in connectionXMLs:
            loaded = ConnectionTypeLoader(self.__addon_storage, connection, file).load()
            connections[loaded.id] = loaded
        
        elements = {}
        for file, element in elementXMLs:
            loaded = ElementTypeLoader(self.__addon_storage, element, file).load()
            elements[loaded.id] = loaded
        
        diagrams = {}
        for file, diagram in diagramXMLs:
            loaded = DiagramTypeLoader(self.__addon_storage, diagram, file, elements, connections).load()
            diagrams[loaded.id] = loaded
        
        templates = []
        for file, template in templateXMLs:
            templates.append(TemplateLoader(template).load())
        
        translations = []
        for file, translation in translationXMLs:
            loaded = TranslationLoader(translation).load()
            translations.append(loaded)
        
        return Metamodel(diagrams, elements, connections, templates, definitions, translations, config)
