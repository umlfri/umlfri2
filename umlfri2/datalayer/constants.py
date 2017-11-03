import os.path

import lxml.etree

from umlfri2.constants.paths import XML_SCHEMAS
from umlfri2.types.version import Version

ADDON_NAMESPACE = 'http://umlfri.org/v2/addon.xsd'
ADDON_SCHEMA = lxml.etree.XMLSchema(lxml.etree.parse(open(os.path.join(XML_SCHEMAS, 'addon', 'addon.xsd'), 'rb')))

ADDON_ADDON_FILE = "addon.xml"
ADDON_DISABLE_FILE = ".disabled"

MODEL_NAMESPACE = 'http://umlfri.org/v2/model.xsd'
MODEL_SCHEMA = lxml.etree.XMLSchema(lxml.etree.parse(open(os.path.join(XML_SCHEMAS, 'model', 'model.xsd'), 'rb')))
MODEL_SAVE_VERSION = Version("2.0")

FRIP2_SOLUTION_FILE = "solution.xml"
FRIP2_PROJECT_FILE = "project/{0}.xml"
FRIP2_MIMETYPE_FILE = "mimetype"
FRIP2_VERSION_FILE = "version"
FRIP2_LOCKED_TABS_FILE = "tabs.xml"

SOLUTION_MIME_TYPE = 'application/vnd.umlfri2.solution'

ONLINE_ADDON_NAMESPACE = 'http://umlfri.org/v2/addon-list.xsd'
ONLINE_ADDON_SCHEMA = lxml.etree.XMLSchema(lxml.etree.parse(open(os.path.join(XML_SCHEMAS, 'addon_list',
                                                                              'addon_list.xsd'), 'rb')))
