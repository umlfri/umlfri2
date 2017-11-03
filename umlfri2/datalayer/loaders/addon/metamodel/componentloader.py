from collections import namedtuple

from ....constants import ADDON_NAMESPACE
from umlfri2.components.all import ALL_COMPONENTS
from umlfri2.components.expressions import UflExpression, ConstantExpression
from umlfri2.ufl.types import UflDefinedEnumType, UflNullableType

ChildAttribute = namedtuple('ChildAttribute', ["name", "type", "values"])


class ComponentLoader:
    def __init__(self, xmlroot, type, definitions={}):
        self.__xmlroot = xmlroot
        self.__type = type
        self.__definitions = definitions
    
    def load(self):
        return list(self.__load_children(self.__xmlroot, self.__type, {}, {}, False))
    
    def __load_children(self, node, component_type, children_attributes, special_children,
                        only_special_children):
        for child in node:
            if child.tag.startswith("{{{0}}}".format(ADDON_NAMESPACE)):
                tagname = child.tag[len(ADDON_NAMESPACE) + 2:]
                
                if tagname in special_children:
                    component = special_children[tagname]
                elif only_special_children:
                    raise Exception("Unknown component")
                else:
                    component = ALL_COMPONENTS[component_type][tagname]
                
                children_params = {}
                params = {}
                for attrname, attrvalue in child.attrib.items():
                    if attrname in children_attributes:
                        type = children_attributes[attrname].type
                        is_children_param = True
                    else:
                        type = component.ATTRIBUTES[attrname]
                        is_children_param = False
                    
                    if isinstance(type, UflDefinedEnumType):
                        if type.name in self.__definitions:
                            type = UflDefinedEnumType(type.type, self.__definitions[type.name])
                    elif isinstance(type, UflNullableType) and isinstance(type.inner_type, UflDefinedEnumType):
                        if type.inner_type.name in self.__definitions:
                            definition = self.__definitions[type.inner_type.name]
                            type = UflNullableType(UflDefinedEnumType(type.inner_type.type, definition))
                    
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
                    if component.CHILDREN_TYPE is None:
                        new_component_type = component_type
                    else:
                        new_component_type = component.CHILDREN_TYPE
                    
                    if component.IS_CONTROL:
                        new_children_attributes = children_attributes
                    else:
                        new_children_attributes = {
                            tagname.lower() + '-' + name: ChildAttribute(name, type, {})
                                for name, type in component.CHILDREN_ATTRIBUTES.items()
                        }
                    
                    new_special_children = component.SPECIAL_CHILDREN
                    new_only_special_children = component.ONLY_SPECIAL_CHILDREN
                    
                    children = list(self.__load_children(child, new_component_type, new_children_attributes,
                                                         new_special_children, new_only_special_children))
                    
                    if not component.IS_CONTROL:
                        for attr in new_children_attributes.values():
                            params[attr.name] = attr.values
                    
                    ret = component(children, **params)
                else:
                    ret = component(**params)
                
                for name, value in children_params.items():
                    children_attributes[name].values[ret] = value
                
                yield ret
