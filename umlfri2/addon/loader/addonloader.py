import lxml.etree

from .addoninfoloader import AddOnInfoLoader
from ..addon import AddOn
from umlfri2.metamodel import Metamodel


class AddOnLoader:
    def __init__(self, path):
        self.__path = path
    
    def load(self):
        info = AddOnInfoLoader(lxml.etree.parse(open(self.__path + '/addon.xml')).getroot()).load()
        
        metamodel = None
        if info.metamodel:
            metamodel = Metamodel(info.config)
        
        return AddOn(info.identifier, info.name, info.version, info.author, info.homepage,
                     info.license, info.icon, info.description, info.config, None,
                     metamodel)
