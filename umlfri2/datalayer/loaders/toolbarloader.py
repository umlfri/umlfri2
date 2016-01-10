from umlfri2.addon.action import AddOnAction
from umlfri2.addon.toolbar import ToolBar
from umlfri2.types.image import Image
from ..constants import ADDON_SCHEMA, ADDON_NAMESPACE


class ToolBarLoader:
    def __init__(self, storage, xmlroot):
        self.__xmlroot = xmlroot
        self.__storage = storage
        
        if not ADDON_SCHEMA.validate(xmlroot):
            raise Exception("Cannot load addon info: {0}".format(ADDON_SCHEMA.error_log.last_error))
    
    def load(self):
        actions = []
        
        for child in self.__xmlroot:
            if child.tag == "{{{0}}}Action".format(ADDON_NAMESPACE):
                icon = None
                if "icon" in child.attrib:
                    icon = Image(self.__storage, child.attrib["icon"])
                actions.append(AddOnAction(child.attrib["id"], icon, child.attrib["label"]))
            else:
                raise Exception
        
        return ToolBar(self.__xmlroot.attrib["label"], actions)
