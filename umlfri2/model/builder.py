from umlfri2.ufl.types import UflObjectType, UflListType, UflFlagsType
from .project import Project


class ProjectBuilder:
    def __init__(self, ruler, template, name="Project"):
        self.__ruler = ruler
        self.__template = template
        self.__name = name
        self.__project = None
        self.__all_objects = {}
    
    @property
    def project(self):
        if self.__project is None:
            self.__build_project()
        return self.__project
    
    def __build_project(self):
        self.__project = Project(self.__template.metamodel, name=self.__name)
        
        for element in self.__template.elements:
            self.__build_element_object(self.__project, element)

        for connection in self.__template.connections:
            self.__build_connection_object(connection)

        for diagram in self.__template.diagrams:
            self.__build_diagram(diagram)
    
    def __build_element_object(self, parent, element):
        ret = parent.create_child_element(element.type)
        
        data = ret.data.make_mutable()
        self.__apply_data(element.type.ufl_type, data, element.data)
        ret.data.apply_patch(data.make_patch())
        
        for child in element.children:
            self.__build_element_object(ret, child)
        
        self.__all_objects[element.id] = ret
        
        return ret

    def __build_connection_object(self, connection):
        source = self.__all_objects[connection.source_id]
        destination = self.__all_objects[connection.destination_id]
        ret = source.connect_with(connection.type, destination)
        
        data = ret.data.make_mutable()
        self.__apply_data(connection.type.ufl_type, data, connection.data)
        ret.data.apply_patch(data.make_patch())
    
    def __build_diagram(self, diagram):
        parent = self.__all_objects[diagram.parent_id]
        ret = parent.create_child_diagram(diagram.type)

        data = ret.data.make_mutable()
        self.__apply_data(diagram.type.ufl_type, data, diagram.data)
        ret.data.apply_patch(data.make_patch())
        
        for element in diagram.elements:
            element_object = self.__all_objects[element.element_id]
            
            element_visual = ret.show(element_object)
            
            if element.position is not None:
                element_visual.move(self.__ruler, element.position)
            
            if element.size is not None:
                element_visual.resize(self.__ruler, element.size)
    
    def __apply_data(self, type, data, values):
        if isinstance(type, UflObjectType):
            self.__apply_object_data(type, data, values)
        elif isinstance(type, UflListType):
            self.__apply_list_data(type, data, values)
        elif isinstance(type, UflFlagsType):
            self.__apply_flags_data(type, data, values)
        else:
            raise Exception
    
    def __apply_object_data(self, type, object, values):
        for name, value in values.items():
            attr_type = type.get_attribute(name).type
            if attr_type.is_immutable:
                object.set_value(name, value)
            else:
                self.__apply_data(attr_type, object.get_value(name), value)
    
    def __apply_list_data(self, type, list, values):
        item_type = type.item_type
        
        if item_type.is_immutable:
            for value in values:
                list.append(value)
        else:
            for value in values:
                row = list.append()
                self.__apply_data(item_type, row, value)
    
    def __apply_flags_data(self, type, flags, values):
        for value in values:
            flags.set(value)
