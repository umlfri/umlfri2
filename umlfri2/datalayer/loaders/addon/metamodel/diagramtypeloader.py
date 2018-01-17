from umlfri2.ufl.components.base.componenttype import ComponentType
from umlfri2.types.image import Image
from .componentloader import ComponentLoader
from ....constants import ADDON_NAMESPACE, ADDON_SCHEMA
from .structureloader import UflStructureLoader
from umlfri2.ufl.components.expressions import LoadedConstantExpression, UflExpression
from umlfri2.ufl.components.text import TextContainerComponent
from umlfri2.metamodel import DiagramType


class DiagramTypeLoader:
    def __init__(self, storage, xmlroot, elements, connections):
        self.__storage = storage
        self.__xmlroot = xmlroot
        if not ADDON_SCHEMA.validate(xmlroot):
            raise Exception("Cannot load diagram type: {0}".format(ADDON_SCHEMA.error_log.last_error))
        self.__elements = elements
        self.__connections = connections
    
    def load(self):
        id = self.__xmlroot.attrib["id"]
        icon = None
        ufl_type = None
        display_name = None
        background = None
        connections = []
        elements = []
        
        for child in self.__xmlroot:
            if child.tag == "{{{0}}}Icon".format(ADDON_NAMESPACE):
                icon_path = child.attrib["path"]
                if not self.__storage.exists(icon_path):
                    raise Exception("Unknown icon {0}".format(icon_path))
                icon = Image(self.__storage, icon_path)
            elif child.tag == "{{{0}}}Structure".format(ADDON_NAMESPACE):
                ufl_type = UflStructureLoader(child).load()
            elif child.tag == "{{{0}}}DisplayName".format(ADDON_NAMESPACE):
                display_name = TextContainerComponent(ComponentLoader(child, ComponentType.text).load())
            elif child.tag == "{{{0}}}Connections".format(ADDON_NAMESPACE):
                for childchild in child:
                    connections.append(childchild.attrib["id"])
            elif child.tag == "{{{0}}}Elements".format(ADDON_NAMESPACE):
                for childchild in child:
                    elements.append(childchild.attrib["id"])
            elif child.tag == "{{{0}}}Appearance".format(ADDON_NAMESPACE):
                for childchild in child:
                    if childchild.tag == "{{{0}}}Background".format(ADDON_NAMESPACE):
                        attrvalue = childchild.attrib["color"]
                        if attrvalue.startswith("##"):
                            background = LoadedConstantExpression(attrvalue[1:])
                        elif attrvalue.startswith("#"):
                            background = UflExpression(attrvalue[1:])
                        else:
                            background = LoadedConstantExpression(attrvalue)
            else:
                raise Exception
        
        elements = tuple(self.__elements[id] for id in elements)
        connections = tuple(self.__connections[id] for id in connections)
        
        return DiagramType(id, icon, ufl_type, display_name, elements, connections, background)
