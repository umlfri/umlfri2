from umlfri2.ufl.components.base.componenttype import ComponentType
from umlfri2.types.image import Image
from .componentloader import ComponentLoader
from ....constants import ADDON_NAMESPACE, ADDON_SCHEMA
from .structureloader import UflStructureLoader
from umlfri2.ufl.components.connectionline import ConnectionVisualContainerComponent
from umlfri2.ufl.components.visual import VisualContainerComponent
from umlfri2.metamodel import ConnectionType
from umlfri2.metamodel.connectiontypelabel import ConnectionTypeLabel
from umlfri2.ufl.types import UflProportionType


class ConnectionTypeLoader:
    def __init__(self, storage, xmlroot):
        self.__storage = storage
        self.__xmlroot = xmlroot
        if not ADDON_SCHEMA.validate(xmlroot):
            raise Exception("Cannot load connection type: {0}".format(ADDON_SCHEMA.error_log.last_error))
    
    def load(self):
        id = self.__xmlroot.attrib["id"]
        icon = None
        ufl_type = None
        appearance = None
        labels = []
        
        for child in self.__xmlroot:
            if child.tag == "{{{0}}}Icon".format(ADDON_NAMESPACE):
                icon_path = child.attrib["path"]
                if not self.__storage.exists(icon_path):
                    raise Exception("Unknown icon {0}".format(icon_path))
                icon = Image(self.__storage, icon_path)
            elif child.tag == "{{{0}}}Structure".format(ADDON_NAMESPACE):
                ufl_type = UflStructureLoader(child).load()
            elif child.tag == "{{{0}}}Appearance".format(ADDON_NAMESPACE):
                appearance_children = list(child)
                
                while appearance_children[-1].tag == "{{{0}}}Label".format(ADDON_NAMESPACE):
                    label = appearance_children[-1]
                    
                    label_position = UflProportionType().parse(label.attrib["position"])
                    label_id = label.attrib["id"]
                    label_appearance = ComponentLoader(label, ComponentType.visual).load()
                    label_appearance = VisualContainerComponent(label_appearance)
                    
                    labels.append(ConnectionTypeLabel(label_position, label_id, label_appearance))
                    
                    del appearance_children[-1]
                
                appearance = ConnectionVisualContainerComponent(ComponentLoader(appearance_children, ComponentType.connection_visual).load())
            else:
                raise Exception
        
        return ConnectionType(id, icon, ufl_type, appearance, labels)
