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
                
                type_name_parser = self.__type_parser.parse(type_name)
                
                type_name_parser.set_default_value_as_string(child.attrib.get("default"))
                
                if type_name_parser.can_have_template and self.__has_template(child):
                    type_name_parser.set_template(self.__load_template(child))
                elif type_name_parser.can_have_possibilities and self.__has_possibilities(child):
                    type_name_parser.set_possibilities(self.__load_possibilities(child))
                elif type_name_parser.can_have_attributes:
                    type_name_parser.set_attributes(self.__load_attributes(child))
                
                yield UflObjectAttribute(child.attrib["id"], type_name_parser.finish())
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
