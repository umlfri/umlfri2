class DiagramTemplate:
    def __init__(self, type, parent_id):
        self.__type = type
        self.__parent_id = parent_id
    
    @property
    def type(self):
        return self.__type
    
    @property
    def parent_id(self):
        return self.__parent_id

    def _compile(self, metamodel):
        self.__type = metamodel.get_diagram_type(self.__type)
