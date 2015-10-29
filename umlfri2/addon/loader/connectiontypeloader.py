from .componentloader import ComponentLoader
from .constants import NAMESPACE
from .structureloader import UflStructureLoader
from umlfri2.components.connectionline import ConnectionLineContainerComponent
from umlfri2.metamodel import ConnectionType
from umlfri2.metamodel.connectiontypelabel import ConnectionTypeLabel
from umlfri2.ufl.types import UflProportionType


class ConnectionTypeLoader:
    def __init__(self, xmlroot):
        self.__xmlroot = xmlroot
    
    def load(self):
        id = self.__xmlroot.attrib["id"]
        icon = None
        ufl_type = None
        appearance = None
        labels = []
        
        for child in self.__xmlroot:
            if child.tag == "{{{0}}}Icon".format(NAMESPACE):
                icon = child.attrib["path"]
            elif child.tag == "{{{0}}}Structure".format(NAMESPACE):
                ufl_type = UflStructureLoader(child).load()
            elif child.tag == "{{{0}}}Appearance".format(NAMESPACE):
                appearance_children = list(child)
                
                while appearance_children[-1].tag == "{{{0}}}Label".format(NAMESPACE):
                    label = appearance_children[-1]
                    
                    label_position = UflProportionType().parse(label.attrib["position"])
                    label_id = label.attrib["id"]
                    label_appearance = ComponentLoader(label, 'visual').load()[0]
                    
                    labels.append(ConnectionTypeLabel(label_position, label_id, label_appearance))
                    
                    del appearance_children[-1]
                
                appearance = ConnectionLineContainerComponent(ComponentLoader(appearance_children, 'connection').load())
            else:
                raise Exception
        
        return ConnectionType(id, icon, ufl_type, appearance, labels)
