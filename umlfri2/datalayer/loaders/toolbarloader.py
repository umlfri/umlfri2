from umlfri2.application.addon.local import AddOnAction, ToolBar, ToolBarItem
from umlfri2.types.image import Image
from ..constants import ADDON_SCHEMA, ADDON_NAMESPACE


class ToolBarLoader:
    def __init__(self, application, storage, xmlroot, actions):
        self.__xmlroot = xmlroot
        self.__storage = storage
        self.__actions = actions
        self.__application = application
        
        if not ADDON_SCHEMA.validate(xmlroot):
            raise Exception("Cannot load addon info: {0}".format(ADDON_SCHEMA.error_log.last_error))
    
    def load(self):
        items = []
        
        for child in self.__xmlroot:
            if child.tag == "{{{0}}}Item".format(ADDON_NAMESPACE):
                icon = None
                if "icon" in child.attrib:
                    icon = Image(self.__storage, child.attrib["icon"])
                
                action_id = child.attrib["action"]
                if action_id in self.__actions:
                    action = self.__actions[action_id]
                else:
                    action = AddOnAction(self.__application, action_id)
                    self.__actions[action_id] = action
                
                items.append(ToolBarItem(action, icon, child.attrib["label"]))
            else:
                raise Exception
        
        return ToolBar(self.__xmlroot.attrib["label"], items)
