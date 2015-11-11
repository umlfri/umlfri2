from .componentloader import ComponentLoader
from .constants import NAMESPACE, ADDON_SCHEMA
from .structureloader import UflStructureLoader
from umlfri2.components.text import TextContainerComponent
from umlfri2.metamodel import ElementType


class ElementTypeLoader:
    def __init__(self, xmlroot):
        self.__xmlroot = xmlroot
        if not ADDON_SCHEMA.validate(xmlroot):
            raise Exception("Cannot load element type: {0}".format(ADDON_SCHEMA.error_log.last_error))
    
    def load(self):
        id = self.__xmlroot.attrib["id"]
        icon = None
        ufl_type = None
        display_name = None
        appearance = None
        
        for child in self.__xmlroot:
            if child.tag == "{{{0}}}Icon".format(NAMESPACE):
                icon = child.attrib["path"]
            elif child.tag == "{{{0}}}Structure".format(NAMESPACE):
                ufl_type = UflStructureLoader(child).load()
            elif child.tag == "{{{0}}}DisplayName".format(NAMESPACE):
                display_name = TextContainerComponent(ComponentLoader(child, 'text').load())
            elif child.tag == "{{{0}}}Appearance".format(NAMESPACE):
                appearance = ComponentLoader(child, 'visual').load()[0]
            else:
                raise Exception
        
        return ElementType(id, icon, ufl_type, display_name, appearance)
