from umlfri2.types.geometry import Point, Size
from umlfri2.ufl.types import UflObjectType, UflListType
from ..constants import MODEL_NAMESPACE, MODEL_SCHEMA
from umlfri2.model import Project


class ProjectLoader:
    # TODO: ignore incorrect attributes
    
    def __init__(self, xmlroot, ruler, addon_manager):
        self.__xmlroot = xmlroot
        if not MODEL_SCHEMA.validate(xmlroot):
            raise Exception("Cannot load project: {0}".format(MODEL_SCHEMA.error_log.last_error))
        
        self.__addon_manager = addon_manager
        self.__connections = []
        self.__visuals = []
        
        self.__element_map = {}
        self.__connection_map = {}
        self.__ruler = ruler
    
    def load(self):
        project = None
        
        for node in self.__xmlroot:
            if node.tag == "{{{0}}}Info".format(MODEL_NAMESPACE):
                project = self.__load_info(node)
            elif node.tag == "{{{0}}}Element".format(MODEL_NAMESPACE):
                self.__load_element(project, project, node)
            else:
                raise Exception
        
        for element, node in self.__connections:
            self.__load_connection(project, element, node)
        
        for diagram, visual in self.__visuals:
            if visual.tag == "{{{0}}}Element".format(MODEL_NAMESPACE):
                self.__load_element_visual(diagram, visual)
            elif visual.tag == "{{{0}}}Connection".format(MODEL_NAMESPACE):
                self.__load_connection_visual(diagram, visual)
        
        return project

    def __load_info(self, node):
        metamodel = None
        metamodel_version = None
        name = None
        
        for child in node:
            if child.tag == "{{{0}}}Name".format(MODEL_NAMESPACE):
                name = child.attrib["name"]
            elif child.tag == "{{{0}}}Metamodel".format(MODEL_NAMESPACE):
                metamodel = child.attrib["id"]
                metamodel_version = child.attrib["version"]
            else:
                raise Exception
        
        # TODO: check version and raise warning if needed
        
        addon = self.__addon_manager.get_addon(metamodel)
        if addon is None or addon.metamodel is None:
            raise Exception("AddOn not found")
        
        return Project(addon.metamodel, name)

    def __load_element(self, project, parent, node):
        type = project.metamodel.get_element_type(node.attrib["type"])
        save_id = node.attrib["id"]
        
        element = parent.create_child_element(type, save_id)
        self.__element_map[element.save_id] = element
        ufl_object = element.data.make_mutable()
        ufl_type = element.type.ufl_type
        
        for child in node:
            if child.tag == "{{{0}}}Element".format(MODEL_NAMESPACE):
                self.__load_element(project, element, child)
            elif child.tag == "{{{0}}}Connection".format(MODEL_NAMESPACE):
                self.__connections.append((element, child))
            elif child.tag == "{{{0}}}Diagram".format(MODEL_NAMESPACE):
                self.__load_diagram(project, element, child)
            elif child.tag == "{{{0}}}Attribute".format(MODEL_NAMESPACE):
                self.__load_ufl_attribute(child, ufl_object, ufl_type)
            else:
                raise Exception
        
        element.apply_ufl_patch(ufl_object.make_patch())
    
    def __load_connection(self, project, element, node):
        type = project.metamodel.get_connection_type(node.attrib["type"])
        save_id = node.attrib["id"]
        to = self.__element_map[node.attrib["to"]]
        
        connection = element.connect_with(type, to, save_id)
        self.__connection_map[connection.save_id] = connection
        ufl_object = connection.data.make_mutable()
        ufl_type = connection.type.ufl_type
        
        for child in node:
            if child.tag == "{{{0}}}Attribute".format(MODEL_NAMESPACE):
                self.__load_ufl_attribute(child, ufl_object, ufl_type)
            else:
                raise Exception
        
        connection.apply_ufl_patch(ufl_object.make_patch())
    
    def __load_diagram(self, project, parent, node):
        type = project.metamodel.get_diagram_type(node.attrib["type"])
        save_id = node.attrib["id"]
        
        diagram = parent.create_child_diagram(type, save_id)
        ufl_object = diagram.data.make_mutable()
        ufl_type = diagram.type.ufl_type
        
        for child in node:
            if child.tag == "{{{0}}}Element".format(MODEL_NAMESPACE):
                self.__visuals.append((diagram, child))
            elif child.tag == "{{{0}}}Connection".format(MODEL_NAMESPACE):
                self.__visuals.append((diagram, child))
            elif child.tag == "{{{0}}}Attribute".format(MODEL_NAMESPACE):
                self.__load_ufl_attribute(child, ufl_object, ufl_type)
            else:
                raise Exception
        
        diagram.apply_ufl_patch(ufl_object.make_patch())

    def __load_ufl(self, ufl_type, node, ufl_object):
        if isinstance(ufl_type, UflObjectType):
            for child in node:
                if child.tag == "{{{0}}}Attribute".format(MODEL_NAMESPACE):
                    self.__load_ufl_attribute(child, ufl_object, ufl_type)
                else:
                    raise Exception
            return None
        elif isinstance(ufl_type, UflListType):
            for child in node:
                if child.tag == "{{{0}}}Item".format(MODEL_NAMESPACE):
                    new_value = ufl_object.append()
                    self.__load_ufl(ufl_type.item_type, child, new_value)
                else:
                    raise Exception
            return None
        else:
            return ufl_type.parse(node.attrib['value'])

    def __load_ufl_attribute(self, child, ufl_object, ufl_type):
        id = child.attrib['id']
        type = ufl_type.get_attribute_type(id)
        current_value = ufl_object.get_value(id)
        new_value = self.__load_ufl(type, child, current_value)
        if new_value is not None:
            ufl_object.set_value(id, new_value)

    def __load_element_visual(self, diagram, node):
        position = Point(int(node.attrib["x"]), int(node.attrib["y"]))
        size = Size(int(node.attrib["width"]), int(node.attrib["height"]))
        element = self.__element_map[node.attrib["id"]]
        
        visual = diagram.show(element)
        visual.move(self.__ruler, position)
        visual.resize(self.__ruler, size)

    def __load_connection_visual(self, diagram, node):
        connection = self.__connection_map[node.attrib["id"]]
        
        visual = diagram.show(connection)
        
        for child in node:
            if child.tag == "{{{0}}}Point".format(MODEL_NAMESPACE):
                position = Point(int(child.attrib["x"]), int(child.attrib["y"]))
                visual.add_point(self.__ruler, None, position)
            else:
                raise Exception
