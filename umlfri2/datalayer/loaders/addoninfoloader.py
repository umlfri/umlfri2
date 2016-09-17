from collections import namedtuple

import re

from umlfri2.application.addon import AddOnDependency, AddOnDependencyType
from ..constants import ADDON_NAMESPACE, ADDON_SCHEMA
from .structureloader import UflStructureLoader
from umlfri2.types.version import Version


AddOnInfo = namedtuple('AddOnInfo', ('identifier', 'name', 'version', 'author', 'homepage', 'license', 'icon',
                                     'description', 'requirements', 'provisions', 'config', 'translations', 'metamodel',
                                     'toolbars', 'patch_module', 'plugin_info'))
PluginInfo = namedtuple('PluginInfo', ('path', 'starter'))


class AddOnInfoLoader:
    __SPACES = re.compile('\\s+')
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
        requirements = set()
        provisions = set()
        config = None
        translations = None
        metamodel = None
        patch_module = None
        plugin_info = None
        toolbars = []
        
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
                        homepage = childchild.attrib["url"]
                    elif childchild.tag == "{{{0}}}CommonLicense".format(ADDON_NAMESPACE):
                        license = childchild.attrib["name"]
                    elif childchild.tag == "{{{0}}}Icon".format(ADDON_NAMESPACE):
                        icon = childchild.attrib["path"]
                    elif childchild.tag == "{{{0}}}Description".format(ADDON_NAMESPACE):
                        description = self.__format_text(childchild.text)
                    else:
                        raise Exception
            elif child.tag == "{{{0}}}Requires".format(ADDON_NAMESPACE):
                requirements = self.__load_dependencies(child)
            elif child.tag == "{{{0}}}Provides".format(ADDON_NAMESPACE):
                provisions = self.__load_dependencies(child)
            elif child.tag == "{{{0}}}Config".format(ADDON_NAMESPACE):
                config = UflStructureLoader(child).load()
            elif child.tag == "{{{0}}}Translations".format(ADDON_NAMESPACE):
                translations = child.attrib["path"]
            elif child.tag == "{{{0}}}ToolBar".format(ADDON_NAMESPACE):
                toolbars.append(child.attrib["path"])
            elif child.tag == "{{{0}}}Metamodel".format(ADDON_NAMESPACE):
                metamodel = child.attrib["path"]
            elif child.tag == "{{{0}}}Patch".format(ADDON_NAMESPACE):
                patch_module = child.attrib["module"]
            elif child.tag == "{{{0}}}Plugin".format(ADDON_NAMESPACE):
                plugin_info = PluginInfo(child.attrib["path"], child.attrib["starter"])
                requirements.add(AddOnDependency(AddOnDependencyType.starter, child.attrib["starter"]))
            else:
                raise Exception
        
        return AddOnInfo(identifier, name, version, author, homepage, license, icon, description, requirements,
                         provisions, config, translations, metamodel, toolbars, patch_module, plugin_info)
    
    def __format_text(self, text):
        current_text = []
        current_line = []
        for line in text.splitlines():
            line = self.__SPACES.sub(' ', line.strip())
            if line:
                current_line.append(line)
            elif current_line:
                current_text.append(' '.join(current_line))
                current_line = []
        return '\n'.join(current_text)

    def __load_dependencies(self, node):
        ret = set()
        for child in node:
            if child.tag == "{{{0}}}Interface".format(ADDON_NAMESPACE):
                ret.add(AddOnDependency(AddOnDependencyType.interface, child.attrib['id']))
            elif child.tag == "{{{0}}}Starter".format(ADDON_NAMESPACE):
                ret.add(AddOnDependency(AddOnDependencyType.starter, child.attrib['id']))
            else:
                raise Exception
        return ret
