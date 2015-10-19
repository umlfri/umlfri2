from umlfri2.ufl.types import *


class UflStructureLoader:
    __simpleTypes = {
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
        attributes = {}
        
        for child in node:
            type = child.attrib["type"]
            
            is_list = False
            if type.endswith("[]"):
                is_list = True
                type = type[:-2]
            
            if type in self.__simpleTypes:
                ufltype = self.__simpleTypes[type]
                default = child.attrib.get("default")
                if default:
                    attr = ufltype(ufltype().parse(default))
                else:
                    attr = ufltype()
            elif type == "enum":
                attr = UflEnumType(self.__load_possibilities(child), child.attrib.get("default"))
            elif type == "object":
                attr = UflObjectType(self.__load_object(child))
            elif type == "str":
                attr = UflStringType(self.__load_possibilities(child), child.attrib.get("default"))
            elif type == "text":
                attr = UflStringType(None, child.attrib.get("default"), True)
            else:
                raise Exception
            
            if is_list:
                attr = UflListType(attr)
            
            attributes[child.attrib["id"]] = attr
        return attributes

    def __load_possibilities(self, node):
        ret = []
        for child in node:
            ret.append(child.attrib["value"])
        
        return ret
