from collections import namedtuple

from umlfri2.application.addon.dependency import AddOnDependency, AddOnDependencyType
from umlfri2.application.addon.license import CommonLicense
from umlfri2.application.addon.online import OnlineAddOnLocation, OnlineAddOnArch, OnlineAddOnVersion
from umlfri2.types.image import Image
from umlfri2.types.version import Version
from ...constants import ONLINE_ADDON_SCHEMA, ONLINE_ADDON_NAMESPACE
from ..textformat import format_text


LoadedAddOnVersion = namedtuple('LoadedAddOnVersion', ['identifier', 'version'])


class OnlineAddOnLoader:
    def __init__(self, xmlroot, storage, path):
        self.__xmlroot = xmlroot
        self.__storage = storage
        self.__path = path
    
    def is_valid(self):
        return ONLINE_ADDON_SCHEMA.validate(self.__xmlroot)
    
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
        changelog = None
        locations = set()
        
        for child in self.__xmlroot:
            if child.tag == "{{{0}}}Name".format(ONLINE_ADDON_NAMESPACE):
                name = child.attrib["name"]
            elif child.tag == "{{{0}}}Version".format(ONLINE_ADDON_NAMESPACE):
                version = Version(child.attrib["version"])
            elif child.tag == "{{{0}}}Author".format(ONLINE_ADDON_NAMESPACE):
                author = child.attrib["name"]
            elif child.tag == "{{{0}}}Homepage".format(ONLINE_ADDON_NAMESPACE):
                homepage = child.attrib["url"]
            elif child.tag == "{{{0}}}CommonLicense".format(ONLINE_ADDON_NAMESPACE):
                license = CommonLicense(child.attrib["name"])
            elif child.tag == "{{{0}}}Icon".format(ONLINE_ADDON_NAMESPACE):
                icon_path = self.__path + '/' + child.attrib["path"]
                if not self.__storage.exists(icon_path):
                    raise Exception("Invalid icon")
                icon = Image(self.__storage, icon_path)
            elif child.tag == "{{{0}}}Description".format(ONLINE_ADDON_NAMESPACE):
                description = format_text(child.text)
            elif child.tag == "{{{0}}}Requires".format(ONLINE_ADDON_NAMESPACE):
                requirements = self.__load_dependencies(child)
            elif child.tag == "{{{0}}}Provides".format(ONLINE_ADDON_NAMESPACE):
                provisions = self.__load_dependencies(child)
            elif child.tag == "{{{0}}}ChangeLog".format(ONLINE_ADDON_NAMESPACE):
                changelog = format_text(child.text)
            elif child.tag == "{{{0}}}InstallFrom".format(ONLINE_ADDON_NAMESPACE):
                locations.add(self.__load_location(child))
            else:
                raise Exception
        
        addon_version = OnlineAddOnVersion(name, version, author, homepage, license, icon, description,
                                              requirements, provisions, changelog, locations)
        
        return LoadedAddOnVersion(identifier, addon_version)
    
    def __load_dependencies(self, node):
        ret = set()
        for child in node:
            if child.tag == "{{{0}}}Interface".format(ONLINE_ADDON_NAMESPACE):
                ret.add(AddOnDependency(AddOnDependencyType.interface, child.attrib['id']))
            elif child.tag == "{{{0}}}Starter".format(ONLINE_ADDON_NAMESPACE):
                ret.add(AddOnDependency(AddOnDependencyType.starter, child.attrib['id']))
            elif child.tag == "{{{0}}}UmlFri".format(ONLINE_ADDON_NAMESPACE):
                pass
            elif child.tag == "{{{0}}}API".format(ONLINE_ADDON_NAMESPACE):
                pass
            elif child.tag == "{{{0}}}MetaMetaModel".format(ONLINE_ADDON_NAMESPACE):
                pass
            else:
                raise Exception
        return ret

    def __load_location(self, child):
        arch = child.attrib.get('arch')
        
        if arch == '32bit':
            arch = OnlineAddOnArch.processor_32
        elif arch == '64bit':
            arch = OnlineAddOnArch.processor_64
        else:
            arch = None
        return OnlineAddOnLocation(child.attrib['url'], child.attrib['sha256'], 'sha256', arch, child.attrib.get('os'))
