import json
from uuid import UUID

from umlfri2.types.geometry import Point, Size
from umlfri2.ufl.types import *


class Snippet:
    __encoder = json.JSONEncoder(ensure_ascii = False, check_circular = False, allow_nan = False)
    __decoder = json.JSONDecoder()
    
    def __init__(self, data):
        self.__data = data
        self.__project_id = UUID(data['project'])
        self.__metamodel_id = data['metamodel']
    
    def serialize(self):
        return self.__encoder.encode(self.__data)
    
    @staticmethod
    def deserialize(data):
        return Snippet(Snippet.__decoder.decode(data))
    
    @property
    def empty(self):
        return len(self.__data['objects']) == 0
    
    def can_be_pasted_to(self, diagram):
        if diagram.project.save_id != self.__project_id:
            return False
        
        ids = set(str(element.object.save_id) for element in diagram.elements)
        
        all_elements = {str(element.save_id): element for element in diagram.project.get_all_elements()}
        all_connections = {str(connection.save_id): connection
                                for element in all_elements.values()
                                    for connection in element.connections}
        
        for obj in self.__data['objects']:
            if obj['kind'] == 'element':
                if obj['id'] not in all_elements:
                    return False
            elif obj['kind'] == 'connection':
                if obj['id'] not in all_connections:
                    return False
        
        for obj in self.__data['objects']:
            if obj['kind'] == 'element':
                if obj['id'] not in ids:
                    return True
        
        return False
    
    def paste_to(self, ruler, diagram):
        all_elements = {str(element.save_id): element for element in diagram.project.get_all_elements()}
        all_connections = {str(connection.save_id): connection
                                for element in all_elements.values()
                                    for connection in element.connections}
        
        for obj in self.__data['objects']:
            if obj['kind'] == 'element':
                o = all_elements[obj['id']]
                if not diagram.contains(o):
                    visual = diagram.show(o)
                    visual.move(ruler, Point(obj['x'], obj['y']))
                    visual.resize(ruler, Size(obj['width'], obj['height']))
                    yield visual
        
        for obj in self.__data['objects']:
            if obj['kind'] == 'connection':
                o = all_connections[obj['id']]
                if not diagram.contains(o):
                    if diagram.contains(o.source) and diagram.contains(o.destination):
                        visual = diagram.show(o)
                        for point in obj['points']:
                            visual.add_point(ruler, None, Point(point['x'], point['y']))
                        for label in visual.get_labels():
                            point = obj['labels'][label.id]
                            label.move(ruler, Point(point['x'], point['y']))
                        yield visual
    
    def can_be_duplicated_to(self, diagram):
        if diagram.project.metamodel.addon.identifier != self.__metamodel_id:
            return False
        
        return True
    
    def duplicate_to(self, ruler, diagram):
        all_elements = {str(element.save_id): element for element in diagram.project.get_all_elements()}
        parent = diagram.parent
        metamodel = diagram.project.metamodel
        
        for obj in self.__data['objects']:
            if obj['kind'] == 'element':
                o = parent.create_child_element(metamodel.get_element_type(obj['type']))
                
                mutable = o.data.make_mutable()
                self.__update_ufl_object(mutable, o.type.ufl_type, obj['data'])
                o.apply_ufl_patch(mutable.make_patch())
                
                all_elements[obj['id']] = o # save object with old id, to make it possible to create connections
                
                visual = diagram.show(o)
                visual.move(ruler, Point(obj['x'], obj['y']))
                visual.resize(ruler, Size(obj['width'], obj['height']))
                yield visual
    
    def __update_ufl_immutable(self, type, input):
        # TODO: font/color/image/etc...
        return input
    
    def __update_ufl_mutable(self, output, type, input):
        if isinstance(type, UflObjectType):
            self.__update_ufl_object(output, type, input)
        elif isinstance(type, UflListType):
            for value in input:
                if type.item_type.is_immutable:
                    output.append(self.__update_ufl_immutable(type.item_type, value))
                else:
                    obj = output.append()
                    self.__update_ufl_mutable(obj, type.item_type, value)
        else:
            raise Exception

    def __update_ufl_object(self, output, ufl_type, input):
        for attribute in ufl_type.attributes:
            if attribute.type.is_immutable:
                output.set_value(attribute.name, self.__update_ufl_immutable(attribute.type, input[attribute.name]))
            else:
                self.__update_ufl_mutable(output.get_value(attribute.name), attribute.type, input[attribute.name])
