from .constants import NAMESPACE
from umlfri2.components.common import COMMON_COMPONENTS
from umlfri2.components.connectionline import CONNECTION_LINE_COMPONENTS
from umlfri2.components.expressions import UflExpression, ConstantExpression
from umlfri2.components.text import TEXT_COMPONENTS
from umlfri2.components.visual import VISUAL_COMPONENTS


class ComponentLoader:
    __components = {}
    __components['visual'] = COMMON_COMPONENTS.copy()
    __components['text'] = COMMON_COMPONENTS.copy()
    __components['connection'] = CONNECTION_LINE_COMPONENTS.copy()
    __components['visual'].update(VISUAL_COMPONENTS)
    __components['text'].update(TEXT_COMPONENTS)
    __components['connection'].update(TEXT_COMPONENTS)
    
    def __init__(self, xmlroot, type):
        self.__xmlroot = xmlroot
        self.__type = type
    
    def load(self):
        return list(self.__load_children(self.__xmlroot, self.__type))
    
    def __load_children(self, node, component_type):
        for child in node:
            if child.tag.startswith("{{{0}}}".format(NAMESPACE)):
                tagname = child.tag[len(NAMESPACE) + 2:]
                
                component = self.__components[component_type][tagname]
                
                params = {}
                for attrname, attrvalue in child.attrib.items():
                    type = component.ATTRIBUTES[attrname]
                    if attrvalue.startswith("##"):
                        value = ConstantExpression(type.parse(attrvalue[1:]), type)
                    elif attrvalue.startswith("#"):
                        value = UflExpression(attrvalue[1:])
                    elif type is str:
                        value = attrvalue
                    else:
                        value = ConstantExpression(type.parse(attrvalue), type)
                    params[attrname] = value
                
                if component.HAS_CHILDREN:
                    children = list(self.__load_children(child, component.CHILDREN_TYPE or component_type))
                    yield component(children, **params)
                else:
                    yield component(**params)
