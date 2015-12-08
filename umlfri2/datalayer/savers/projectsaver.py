import lxml.etree

from umlfri2.ufl.types import UflObjectType, UflListType
from ..constants import MODEL_NAMESPACE, MODEL_SAVE_VERSION, MODEL_SCHEMA


class ProjectSaver:
    def __init__(self, storage, path, ruler):
        self.__storage = storage
        self.__path = path
        self.__ruler = ruler
    
    def save(self, project):
        root = lxml.etree.Element('{{{0}}}Project'.format(MODEL_NAMESPACE), nsmap={None: MODEL_NAMESPACE})
        root.attrib['id'] = str(project.save_id)
        root.attrib['saveversion'] = str(MODEL_SAVE_VERSION)
        
        name = lxml.etree.Element('{{{0}}}Name'.format(MODEL_NAMESPACE))
        name.attrib['name'] = project.name
        
        metamodel = lxml.etree.Element('{{{0}}}Metamodel'.format(MODEL_NAMESPACE))
        metamodel.attrib['id'] = project.metamodel.addon.identifier
        metamodel.attrib['version'] = str(project.metamodel.addon.version)
        
        info = lxml.etree.Element('{{{0}}}Info'.format(MODEL_NAMESPACE))
        info.append(name)
        info.append(metamodel)
        root.append(info)
        
        for element in project.children:
            root.append(self.__element_to_xml(element))
        
        if not MODEL_SCHEMA.validate(root):
            raise Exception("Cannot save project! {0}".format(MODEL_SCHEMA.error_log.last_error))
        
        tree = lxml.etree.ElementTree(root)
        with self.__storage.open(self.__path, "w") as file:
            tree.write(file, pretty_print=True, encoding="UTF-8", xml_declaration=True)
    
    def __element_to_xml(self, element):
        xml = lxml.etree.Element('{{{0}}}Element'.format(MODEL_NAMESPACE))
        xml.attrib['id'] = str(element.save_id)
        xml.attrib['type'] = element.type.id
        
        self.__save_ufl_object(xml, element.data, element.type.ufl_type)
        
        for diagram in element.diagrams:
            xml.append(self.__diagram_to_xml(diagram))
        
        for child in element.children:
            xml.append(self.__element_to_xml(child))
        
        for connection in element.connections:
            if connection.source is element:
                xml.append(self.__connection_to_xml(connection))
        
        return xml
    
    def __connection_to_xml(self, connection):
        xml = lxml.etree.Element('{{{0}}}Connection'.format(MODEL_NAMESPACE))
        xml.attrib['id'] = str(connection.save_id)
        xml.attrib['type'] = connection.type.id
        xml.attrib['to'] = str(connection.destination.save_id)
        
        self.__save_ufl_object(xml, connection.data, connection.type.ufl_type)
        
        return xml
    
    def __diagram_to_xml(self, diagram):
        xml = lxml.etree.Element('{{{0}}}Diagram'.format(MODEL_NAMESPACE))
        xml.attrib['id'] = str(diagram.save_id)
        xml.attrib['type'] = diagram.type.id
        
        self.__save_ufl_object(xml, diagram.data, diagram.type.ufl_type)
        
        for element in diagram.elements:
            element_xml = lxml.etree.Element('{{{0}}}Element'.format(MODEL_NAMESPACE))
            element_xml.attrib['id'] = str(element.object.save_id)
            position = element.get_position(self.__ruler)
            size = element.get_size(self.__ruler)
            element_xml.attrib['x'] = str(position.x)
            element_xml.attrib['y'] = str(position.y)
            element_xml.attrib['width'] = str(size.width)
            element_xml.attrib['height'] = str(size.height)
            xml.append(element_xml)
        
        for connection in diagram.connections:
            connection_xml = lxml.etree.Element('{{{0}}}Connection'.format(MODEL_NAMESPACE))
            connection_xml.attrib['id'] = str(connection.object.save_id)
            
            for point in connection.get_points(self.__ruler, source_and_end=False):
                point_xml = lxml.etree.Element('{{{0}}}Point'.format(MODEL_NAMESPACE))
                point_xml.attrib['x'] = str(point.x)
                point_xml.attrib['y'] = str(point.y)
                connection_xml.append(point_xml)
            xml.append(connection_xml)
        
        return xml
    
    def __save_ufl_any(self, xml, value, type):
        if isinstance(type, UflObjectType):
            self.__save_ufl_object(xml, value, type)
        elif isinstance(type, UflListType):
            self.__save_ufl_list(xml, value, type)
        else:
            xml.attrib['value'] = str(value)
    
    def __save_ufl_object(self, xml, value, type):
        for attr in type.attributes:
            attr_value = value.get_value(attr.name)
            if not attr.type.is_default_value(attr_value):
                attr_xml = lxml.etree.Element('{{{0}}}Attribute'.format(MODEL_NAMESPACE))
                attr_xml.attrib['id'] = attr.name
                self.__save_ufl_any(attr_xml, attr_value, attr.type)
                xml.append(attr_xml)
    
    
    def __save_ufl_list(self, xml, value, type):
        for item_value in value:
            item_xml = lxml.etree.Element('{{{0}}}Item'.format(MODEL_NAMESPACE))
            if not type.item_type.is_default_value(item_value):
                self.__save_ufl_any(item_xml, item_value, type.item_type)
            xml.append(item_xml)
