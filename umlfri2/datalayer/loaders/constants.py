import lxml.etree
import os.path
from umlfri2.paths import XML_SCHEMAS

NAMESPACE = 'http://umlfri.org/v2/addon.xsd'

ADDON_SCHEMA = lxml.etree.XMLSchema(lxml.etree.parse(open(os.path.join(XML_SCHEMAS, 'addon', 'addon.xsd'), 'rb')))
