import lxml.etree

from ..constants import MODEL_NAMESPACE, MODEL_SCHEMA


class LockedTabsSaver:
    def __init__(self, storage, path):
        self.__storage = storage
        self.__path = path
    
    def save(self, locked_tabs):
        root = lxml.etree.Element('{{{0}}}Tabs'.format(MODEL_NAMESPACE), nsmap={None: MODEL_NAMESPACE})
        
        for tab in locked_tabs:
            tab_xml = lxml.etree.Element('{{{0}}}Tab'.format(MODEL_NAMESPACE))
            tab_xml.attrib["diagram"] = str(tab.drawing_area.diagram.save_id)
            tab_xml.attrib["locked"] = 'true'
            root.append(tab_xml)
        
        if not MODEL_SCHEMA.validate(root):
            raise Exception("Cannot save solution! {0}".format(MODEL_SCHEMA.error_log.last_error))
        
        tree = lxml.etree.ElementTree(root)
        with self.__storage.open(self.__path, "w") as file:
            tree.write(file, pretty_print=True, encoding="UTF-8", xml_declaration=True)
