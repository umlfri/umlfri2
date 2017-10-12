from .empty import EmptyObject
from .visualcomponent import VisualComponent


class SimpleComponent(VisualComponent):
    def _create_object(self, context, ruler):
        for local, child in self._get_children(context):
            return child._create_object(local, ruler)
        
        return EmptyObject()
    
    def compile(self, type_context):
        self._compile_children(type_context)
