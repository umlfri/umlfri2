from collections import OrderedDict

from umlfri2.components.base.componenttype import ComponentType
from umlfri2.components.base.typecontext import TypeContext
from ....constants import ADDON_NAMESPACE
from .componentloader import ComponentLoader
from umlfri2.components.text import TextContainerComponent
from umlfri2.ufl.types import UflTypeParser, UflObjectType, UflObjectAttribute, UflStringType, UflIntegerType


class UflStructureLoader:
    def __init__(self, xmlroot):
        self.__xmlroot = xmlroot
        self.__type_parser = UflTypeParser()
    
    def load(self):
        return UflObjectType(self.__load_attributes(self.__xmlroot))

    def __load_attributes(self, node):
        for child in node:
            if child.tag == "{{{0}}}Attribute".format(ADDON_NAMESPACE):
                type_name = child.attrib["type"]
    
                default = self.__type_parser.parse_default_value(type_name, child.attrib.get("default"))
                
                if self.__type_parser.has_template(type_name) and self.__has_template(child):
                    if default is not None:
                        raise Exception("Cannot have both default value and template")
                    child_template = self.__load_template(child)
                    attr_type = self.__type_parser.parse_with_template(type_name, child_template)
                elif self.__type_parser.has_possibilities(type_name) and self.__has_possibilities(child):
                    child_possibilities = self.__load_possibilities(child)
                    attr_type = self.__type_parser.parse_with_possibilities_and_default(type_name, child_possibilities, default)
                elif self.__type_parser.has_attributes(type_name):
                    if default is not None:
                        raise Exception("Object types cannot have default value specified")
                    child_attributes = self.__load_attributes(child)
                    attr_type = self.__type_parser.parse_with_attributes(type_name, child_attributes)
                else:
                    attr_type = self.__type_parser.parse_with_default(type_name, default)
                
                yield UflObjectAttribute(child.attrib["id"], attr_type)
            else:
                raise Exception
    
    def __has_possibilities(self, node):
        return node.find("{{{0}}}Value".format(ADDON_NAMESPACE)) is not None
    
    def __load_possibilities(self, node):
        for child in node:
            if child.tag == "{{{0}}}Value".format(ADDON_NAMESPACE):
                yield child.attrib["value"]
            else:
                raise Exception
    
    def __has_template(self, node):
        return node.find("{{{0}}}Template".format(ADDON_NAMESPACE)) is not None

    def __load_template(self, node):
        for child in node:
            if child.tag == "{{{0}}}Template".format(ADDON_NAMESPACE):
                template = TextContainerComponent(ComponentLoader(child, ComponentType.text).load())
                type_context = TypeContext()\
                    .set_variable_type('parent', UflStringType())\
                    .set_variable_type('no', UflIntegerType())
                template.compile(type_context)
                return template
            else:
                raise Exception
        
        return None
