from collections import OrderedDict

from ..constants import ADDON_NAMESPACE
from .componentloader import ComponentLoader
from umlfri2.components.text import TextContainerComponent
from umlfri2.ufl.types import *


class UflStructureLoader:
    __simple_types = {
        "bool": UflBoolType,
        "color": UflColorType,
        "font": UflFontType,
        "int": UflIntegerType,
    }
    
    def __init__(self, xmlroot):
        self.__xmlroot = xmlroot
    
    def load(self):
        return UflObjectType(self.__load_object(self.__xmlroot))

    def __load_object(self, node):
        attributes = OrderedDict()
        
        for child in node:
            type = child.attrib["type"]
            
            is_list = False
            if type.endswith("[]"):
                is_list = True
                type = type[:-2]
            
            if type in self.__simple_types:
                ufltype = self.__simple_types[type]
                default = child.attrib.get("default")
                if default:
                    attr = ufltype(ufltype().parse(default))
                else:
                    attr = ufltype()
            elif type == "enum":
                attr = UflStringEnumType(self.__load_possibilities(child) or (), child.attrib.get("default"))
            elif type == "object":
                attr = UflObjectType(self.__load_object(child))
            elif type == "str":
                attr = UflStringType(self.__load_possibilities(child) or None, child.attrib.get("default"), self.__load_template(child))
            elif type == "text":
                attr = UflStringType(None, child.attrib.get("default"), multiline=True)
            else:
                raise Exception
            
            if is_list:
                attr = UflListType(attr)
            
            attributes[child.attrib["id"]] = UflObjectAttribute(child.attrib["id"], attr)
        return attributes

    def __load_possibilities(self, node):
        ret = []
        for child in node:
            if child.tag == "{{{0}}}Value".format(ADDON_NAMESPACE):
                ret.append(child.attrib["value"])
        
        return ret

    def __load_template(self, node):
        for child in node:
            if child.tag == "{{{0}}}Template".format(ADDON_NAMESPACE):
                template = TextContainerComponent(ComponentLoader(child, 'text').load())
                template.compile({'parent': UflStringType(), 'no': UflIntegerType()})
                return template
        
        return None
