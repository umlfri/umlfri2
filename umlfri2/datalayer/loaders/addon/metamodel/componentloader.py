from collections import namedtuple

from ....constants import ADDON_NAMESPACE
from umlfri2.ufl.components.all import ALL_COMPONENTS
from umlfri2.ufl.components.expressions import UflExpression, LoadedConstantExpression

ChildAttribute = namedtuple('ChildAttribute', ["name", "type", "values"])


class ComponentLoader:
    def __init__(self, xmlroot, type):
        self.__xmlroot = xmlroot
        self.__type = type
    
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
                        is_str = children_attributes[attrname].type is str
                        is_children_param = True
                    else:
                        is_str = component.ATTRIBUTES[attrname] is str
                        is_children_param = False
                    
                    if is_str:
                        value = attrvalue
                    elif attrvalue.startswith("##"):
                        value = LoadedConstantExpression(attrvalue[1:])
                    elif attrvalue.startswith("#"):
                        value = UflExpression(attrvalue[1:])
                    else:
                        value = LoadedConstantExpression(attrvalue)
                    
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
