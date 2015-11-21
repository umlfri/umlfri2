import lxml.etree
import os.path
from umlfri2.paths import XML_SCHEMAS

ADDON_NAMESPACE = 'http://umlfri.org/v2/addon.xsd'
ADDON_SCHEMA = lxml.etree.XMLSchema(lxml.etree.parse(open(os.path.join(XML_SCHEMAS, 'addon', 'addon.xsd'), 'rb')))

MODEL_NAMESPACE = 'http://umlfri.org/v2/model.xsd'
MODEL_SCHEMA = lxml.etree.XMLSchema(lxml.etree.parse(open(os.path.join(XML_SCHEMAS, 'model', 'model.xsd'), 'rb')))
