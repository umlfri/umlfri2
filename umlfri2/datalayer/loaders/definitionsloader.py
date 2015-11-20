import math

from ..constants import NAMESPACE, ADDON_SCHEMA
from umlfri2.components.connectionline.arrow import ArrowDefinition
from umlfri2.types.geometry import PathBuilder, Point


class DefinitionsLoader:
    def __init__(self, xmlroot):
        self.__xmlroot = xmlroot
        if not ADDON_SCHEMA.validate(xmlroot):
            raise Exception("Cannot load definitions: {0}".format(ADDON_SCHEMA.error_log.last_error))
    
    def load(self):
        definitions = {
            "ArrowDefinition": {},
            "CornerDefinition": {},
            "SideDefinition": {},
        }
        
        for child in self.__xmlroot:
            if child.tag == "{{{0}}}ArrowDefinition".format(NAMESPACE):
                definition = ArrowDefinition(
                    child.attrib["id"],
                    PathBuilder().from_string(child.attrib["path"]).build(),
                    Point.parse(child.attrib["center"]),
                    self.__parse_rotation(child.attrib["rotation"])
                )
                definitions["ArrowDefinition"][definition.id] = definition
        
        return definitions

    def __parse_rotation(self, value):
        if value.endswith("°"):
            return int(value[:-1]) * math.pi / 180
        else:
            return float(value)
