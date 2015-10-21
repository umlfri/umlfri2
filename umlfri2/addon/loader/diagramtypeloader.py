from .componentloader import ComponentLoader
from .constants import NAMESPACE
from .structureloader import UflStructureLoader
from umlfri2.components.expressions import ConstantExpression, UflExpression
from umlfri2.components.text import TextContainer
from umlfri2.addon.metamodel import DiagramType
from umlfri2.types.color import Color


class DiagramTypeLoader:
    def __init__(self, metamodel, xmlroot):
        self.__metamodel = metamodel
        self.__xmlroot = xmlroot
    
    def load(self):
        id = self.__xmlroot.attrib["id"]
        icon = None
        ufl_type = None
        display_name = None
        background = None
        connections = []
        elements = []
        
        for child in self.__xmlroot:
            if child.tag == "{{{0}}}Icon".format(NAMESPACE):
                icon = child.attrib["path"]
            elif child.tag == "{{{0}}}Structure".format(NAMESPACE):
                ufl_type = UflStructureLoader(child).load()
            elif child.tag == "{{{0}}}DisplayName".format(NAMESPACE):
                display_name = TextContainer(ComponentLoader(child, 'text').load())
            elif child.tag == "{{{0}}}Connections".format(NAMESPACE):
                for childchild in child:
                    connections.append(childchild.attrib["id"])
            elif child.tag == "{{{0}}}Elements".format(NAMESPACE):
                for childchild in child:
                    elements.append(childchild.attrib["id"])
            elif child.tag == "{{{0}}}Appearance".format(NAMESPACE):
                for childchild in child:
                    if childchild.tag == "{{{0}}}Background".format(NAMESPACE):
                        attrvalue = childchild.attrib["color"]
                        if attrvalue.startswith("##"):
                            background = ConstantExpression(Color.get_color(attrvalue[1:]), Color)
                        elif attrvalue.startswith("#"):
                            background = UflExpression(attrvalue[1:])
                        else:
                            background = ConstantExpression(Color.get_color(attrvalue[1:]), Color)
            else:
                raise Exception
        
        # TODO: link associated elements and connections to diagram type
        return DiagramType(self.__metamodel, id, icon, ufl_type, display_name, (), (), background)
