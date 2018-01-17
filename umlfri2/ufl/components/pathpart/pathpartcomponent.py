from ..base.component import Component

class PathPartComponent(Component):
    HAS_CHILDREN = False
    
    def __init__(self):
        super().__init__(())
    
    def add_to_path(self, context, builder):
        raise NotImplementedError
