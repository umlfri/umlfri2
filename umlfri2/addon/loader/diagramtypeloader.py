from .componentloader import ComponentLoader
from .constants import NAMESPACE
from .structureloader import UflStructureLoader
from umlfri2.components.expressions import ConstantExpression, UflExpression
from umlfri2.components.text import TextContainerComponent
from umlfri2.metamodel import DiagramType
from umlfri2.types.color import Color


class DiagramTypeLoader:
    def __init__(self, xmlroot, elements, connections):
        self.__xmlroot = xmlroot
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
            if child.tag == "{{{0}}}Icon".format(NAMESPACE):
                icon = child.attrib["path"]
            elif child.tag == "{{{0}}}Structure".format(NAMESPACE):
                ufl_type = UflStructureLoader(child).load()
            elif child.tag == "{{{0}}}DisplayName".format(NAMESPACE):
                display_name = TextContainerComponent(ComponentLoader(child, 'text').load())
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
        
        
        elements = tuple(self.__elements[id] for id in elements)
        #connections = tuple(self.__connections[id] for id in connections)
        connections = () # TODO
        
        return DiagramType(id, icon, ufl_type, display_name, elements, connections, background)
