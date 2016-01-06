import json
from uuid import UUID

from umlfri2.types.geometry import Point, Size


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
        
        all_element_ids = set(str(element.save_id) for element in diagram.project.get_all_elements())
        
        for obj in self.__data['objects']:
            if obj['kind'] == 'element':
                if obj['id'] not in all_element_ids:
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
