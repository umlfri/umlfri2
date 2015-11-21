from collections import namedtuple

from ..constants import ADDON_NAMESPACE, ADDON_SCHEMA
from .structureloader import UflStructureLoader
from umlfri2.types.version import Version


AddOnInfo = namedtuple('AddOnInfo', ('identifier', 'name', 'version', 'author', 'homepage', 'license', 'icon', 'description', 'config', 'translations', 'metamodel'))


class AddOnInfoLoader:
    def __init__(self, xmlroot):
        self.__xmlroot = xmlroot
        if not ADDON_SCHEMA.validate(xmlroot):
            raise Exception("Cannot load addon info: {0}".format(ADDON_SCHEMA.error_log.last_error))
    
    def load(self):
        identifier = self.__xmlroot.attrib['id']
        name = None
        version = None
        author = None
        homepage = None
        license = None
        icon = None
        description = None
        config = None
        translations = None
        metamodel = None
        
        for child in self.__xmlroot:
            if child.tag == "{{{0}}}AddOnInfo".format(ADDON_NAMESPACE):
                for childchild in child:
                    if childchild.tag == "{{{0}}}Name".format(ADDON_NAMESPACE):
                        name = childchild.attrib["name"]
                    elif childchild.tag == "{{{0}}}Version".format(ADDON_NAMESPACE):
                        version = Version(childchild.attrib["version"])
                    elif childchild.tag == "{{{0}}}Author".format(ADDON_NAMESPACE):
                        author = childchild.attrib["name"]
                    elif childchild.tag == "{{{0}}}Homepage".format(ADDON_NAMESPACE):
                        author = childchild.attrib["url"]
                    elif childchild.tag == "{{{0}}}CommonLicense".format(ADDON_NAMESPACE):
                        license = childchild.attrib["name"]
                    elif childchild.tag == "{{{0}}}Icon".format(ADDON_NAMESPACE):
                        icon = childchild.attrib["path"]
                    elif childchild.tag == "{{{0}}}Description".format(ADDON_NAMESPACE):
                        description = childchild.text
                    else:
                        raise Exception
            elif child.tag == "{{{0}}}Config".format(ADDON_NAMESPACE):
                config = UflStructureLoader(child).load()
            elif child.tag == "{{{0}}}Translations".format(ADDON_NAMESPACE):
                translations = None # TODO
            elif child.tag == "{{{0}}}Metamodel".format(ADDON_NAMESPACE):
                metamodel = child.attrib["path"]
            else:
                raise Exception
        
        return AddOnInfo(identifier, name, version, author, homepage, license, icon, description, config, translations, metamodel)
