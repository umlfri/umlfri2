class Component:
    def __init__(self, children):
        self.__children = children
        self.__parent = None
        
        for child in children:
            child.__parent = self
    
    def is_control(self):
        raise NotImplementedError
    
    def _get_children(self, context):
        for child in self.__children:
            if child.is_control():
                yield from child.filter_children(context)
            else:
                yield context, child
    
    def _get_parent(self):
        return self.__parent
