from umlfri2.metamodel.loader.constants import NAMESPACE
from umlfri2.metamodel.loader.structureloader import UflStructureLoader
from umlfri2.metamodel.metamodel import Metamodel


class AddonInfoLoader:
    def __init__(self, xmlroot):
        self.__xmlroot = xmlroot
    
    def load(self):
        config = None
        
        for child in self.__xmlroot:
            if child.tag == "{{{0}}}Config".format(NAMESPACE):
                config = UflStructureLoader(child).load()
        
        return Metamodel(config)
