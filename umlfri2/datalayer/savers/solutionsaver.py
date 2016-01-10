import lxml.etree

from ..constants import MODEL_NAMESPACE, MODEL_SCHEMA


class SolutionSaver:
    def __init__(self, storage, path):
        self.__storage = storage
        self.__path = path
    
    def save(self, solution):
        root = lxml.etree.Element('{{{0}}}Solution'.format(MODEL_NAMESPACE), nsmap={None: MODEL_NAMESPACE})
        root.attrib["id"] = str(solution.save_id)
        
        for project in solution.children:
            project_xml = lxml.etree.Element('{{{0}}}Project'.format(MODEL_NAMESPACE))
            project_xml.attrib["id"] = str(project.save_id)
            root.append(project_xml)
        
        if not MODEL_SCHEMA.validate(root):
            raise Exception("Cannot save solution! {0}".format(MODEL_SCHEMA.error_log.last_error))
        
        tree = lxml.etree.ElementTree(root)
        with self.__storage.open(self.__path, "w") as file:
            tree.write(file, pretty_print=True, encoding="UTF-8", xml_declaration=True)
