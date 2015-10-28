from .constants import NAMESPACE
from umlfri2.components.common import COMMON_COMPONENTS, SWITCH_COMPONENTS
from umlfri2.components.connectionline import CONNECTION_LINE_COMPONENTS
from umlfri2.components.expressions import UflExpression, ConstantExpression
from umlfri2.components.text import TEXT_COMPONENTS
from umlfri2.components.visual import VISUAL_COMPONENTS, TABLE_COMPONENTS


class ComponentLoader:
    __components = {}
    
    __components['visual'] = COMMON_COMPONENTS.copy()
    __components['table'] = COMMON_COMPONENTS.copy()
    __components['text'] = COMMON_COMPONENTS.copy()
    __components['connection'] = COMMON_COMPONENTS.copy()
    
    __components['switch'] = SWITCH_COMPONENTS.copy()
    
    __components['visual'].update(VISUAL_COMPONENTS)
    __components['text'].update(TEXT_COMPONENTS)
    __components['connection'].update(CONNECTION_LINE_COMPONENTS)
    __components['table'].update(TABLE_COMPONENTS)
    
    def __init__(self, xmlroot, type):
        self.__xmlroot = xmlroot
        self.__type = type
    
    def load(self):
        return list(self.__load_children(self.__xmlroot, self.__type, (self.__type, )))
    
    def __load_children(self, node, component_type, previous_types):
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
                    if component.CHILDREN_TYPE == 'return':
                        new_component_type = previous_types[-1]
                        new_previous_types = previous_types[:-1]
                    elif component.CHILDREN_TYPE is not None:
                        new_component_type = component.CHILDREN_TYPE
                        new_previous_types = previous_types + (new_component_type, )
                    else:
                        new_component_type = component_type
                        new_previous_types = previous_types
                    
                    children = list(self.__load_children(child, new_component_type, new_previous_types))
                    yield component(children, **params)
                else:
                    yield component(**params)
