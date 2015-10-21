from .componentloader import ComponentLoader
from .constants import NAMESPACE
from .structureloader import UflStructureLoader
from umlfri2.components.text import TextContainer
from umlfri2.addon.metamodel import ElementType


class ElementTypeLoader:
    def __init__(self, metamodel, xmlroot):
        self.__metamodel = metamodel
        self.__xmlroot = xmlroot
    
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
                display_name = TextContainer(ComponentLoader(child, 'text').load())
            elif child.tag == "{{{0}}}Appearance".format(NAMESPACE):
                appearance = ComponentLoader(child, 'visual').load()[0]
            else:
                raise Exception
        
        return ElementType(self.__metamodel, id, icon, ufl_type, display_name, appearance)
