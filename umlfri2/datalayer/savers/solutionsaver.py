import lxml.etree

from ..constants import MODEL_NAMESPACE


class SolutionSaver:
    def __init__(self, storage, path):
        self.__storage = storage
        self.__path = path
    
    def save(self, solution):
        root = lxml.etree.Element('{{{0}}}Solution'.format(MODEL_NAMESPACE), nsmap={None: MODEL_NAMESPACE})
        
        for project in solution.children:
            project_xml = lxml.etree.Element('{{{0}}}Project'.format(MODEL_NAMESPACE))
            project_xml.attrib["id"] = str(project.save_id)
            root.append(project_xml)
        
        tree = lxml.etree.ElementTree(root)
        tree.write(self.__storage.open(self.__path, "w"), pretty_print=True, encoding="UTF-8", xml_declaration=True)
