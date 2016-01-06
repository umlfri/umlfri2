import json
from uuid import UUID


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
        # TODO: each element in snippet must exist in the project
        if diagram.project.save_id != self.__project_id:
            return False
        
        ids = set(obj['id'] for obj in self.__data['objects'])
        
        for element in diagram.elements:
            if element.object.save_id not in ids:
                return True
        
        return False
