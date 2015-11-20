from collections import namedtuple

from ..constants import NAMESPACE
from umlfri2.components.common import COMMON_COMPONENTS, SWITCH_COMPONENTS
from umlfri2.components.connectionline import CONNECTION_LINE_COMPONENTS
from umlfri2.components.expressions import UflExpression, ConstantExpression
from umlfri2.components.text import TEXT_COMPONENTS
from umlfri2.components.visual import VISUAL_COMPONENTS, TABLE_COMPONENTS
from umlfri2.ufl.types import UflDefinedEnumType


ChildAttribute = namedtuple('ChildAttribute', ["name", "type", "values"])


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
    
    def __init__(self, xmlroot, type, definitions={}):
        self.__xmlroot = xmlroot
        self.__type = type
        self.__definitions = definitions
    
    def load(self):
        return list(self.__load_children(self.__xmlroot, self.__type, (), {}))
    
    def __load_children(self, node, component_type, previous_types, children_attributes):
        for child in node:
            if child.tag.startswith("{{{0}}}".format(NAMESPACE)):
                tagname = child.tag[len(NAMESPACE) + 2:]
                
                component = self.__components[component_type][tagname]
                
                children_params = {}
                params = {}
                for attrname, attrvalue in child.attrib.items():
                    if attrname in children_attributes:
                        type = children_attributes[attrname].type
                        is_children_param = True
                    else:
                        type = component.ATTRIBUTES[attrname]
                        is_children_param = False
                    
                    if isinstance(type, UflDefinedEnumType) and type.name in self.__definitions:
                        type = UflDefinedEnumType(type.type, self.__definitions[type.name])
                    
                    if attrvalue.startswith("##"):
                        value = ConstantExpression(type.parse(attrvalue[1:]), type)
                    elif attrvalue.startswith("#"):
                        value = UflExpression(attrvalue[1:])
                    elif type is str:
                        value = attrvalue
                    else:
                        value = ConstantExpression(type.parse(attrvalue), type)
                    
                    if is_children_param:
                        children_params[attrname] = value
                    else:
                        params[attrname] = value
                
                if component.HAS_CHILDREN:
                    if component.CHILDREN_TYPE == 'return':
                        new_component_type = previous_types[-1]
                        new_previous_types = previous_types[:-1]
                    elif component.CHILDREN_TYPE is not None:
                        new_component_type = component.CHILDREN_TYPE
                        new_previous_types = previous_types + (component_type, )
                    else:
                        new_component_type = component_type
                        new_previous_types = previous_types
                    
                    if component.IS_CONTROL:
                        new_children_attributes = children_attributes
                    else:
                        new_children_attributes = {
                            tagname.lower() + '-' + name: ChildAttribute(name, type, {})
                                for name, type in component.CHILDREN_ATTRIBUTES.items()
                        }
                    
                    children = list(self.__load_children(child, new_component_type, new_previous_types, new_children_attributes))
                    
                    if not component.IS_CONTROL:
                        for attr in new_children_attributes.values():
                            params[attr.name] = attr.values
                    
                    ret = component(children, **params)
                else:
                    ret = component(**params)
                
                for name, value in children_params.items():
                    children_attributes[name].values[ret] = value
                
                yield ret
