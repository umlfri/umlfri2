from .basecontainer import BaseContainer


class Namespace(BaseContainer):
    def __init__(self, name, parent):
        BaseContainer.__init__(self, name, parent)
    
    @property
    def descendants(self):
        for child in self.children:
            yield child
            if isinstance(child, Namespace):
                for grand_descendant in child.descendants:
                    yield grand_descendant
    
    def descendants_of_type(self, *type_names):
        for child in self.children:
            if child.type_name in type_names:
                yield child
            if isinstance(child, Namespace):
                for grand_descendant in child.descendants_of_type(*type_names):
                    yield grand_descendant
