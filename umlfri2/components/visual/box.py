from collections import namedtuple
from umlfri2.types.geometry import Size, Rectangle
from umlfri2.ufl.types import UflBoolType
from .visualcomponent import VisualComponent, VisualObject


BoxChild = namedtuple('BoxChild', ["child", "expand"])


class BoxObject(VisualObject):
    def __init__(self, children):
        self.__children = children
        
        self.__children_sizes = [child.child.get_minimal_size() for child in children]
    
    def _new_size(self, size, whole_size, delta):
        raise NotImplementedError
    
    def _new_position(self, position, size):
        raise NotImplementedError
    
    def _compute_size(self, all_widths, all_heights):
        raise NotImplementedError
    
    def _get_size_component(self, size):
        raise NotImplementedError
    
    def _get_default_resizable(self):
        raise NotImplementedError
    
    def assign_bounds(self, bounds):
        position = bounds.top_left
        whole_size = bounds.size
        
        if self.__children:
            deltas = self.__compute_deltas(
                [self._get_size_component(size) for size in self.__children_sizes],
                self._get_size_component(whole_size)
            )
            for size, delta, child in zip(self.__children_sizes, deltas, self.__children):
                child.child.assign_bounds(Rectangle.from_point_size(position, self._new_size(size, whole_size, delta)))
                position = self._new_position(position, size)
    
    def get_minimal_size(self):
        if self.__children_sizes:
            return self._compute_size((s.width for s in self.__children_sizes),
                                      (s.height for s in self.__children_sizes))
        else:
            return Size(0, 0)
    
    def __compute_deltas(self, sizes, whole):
        to_expand = []
        cnt = 0
        for index, child in enumerate(self.__children):
            if child.expand:
                cnt += 1
                to_expand.append(index)
        
        deltas = [0] * len(sizes)
        
        if to_expand:
            extra_size = whole - sum(sizes)
            
            delta_size = extra_size // cnt
            
            for index in to_expand:
                deltas[index] = delta_size
            
            deltas[to_expand[-1]] += extra_size - delta_size*cnt
        
        return deltas
    
    def draw(self, canvas, shadow):
        for child in self.__children:
            child.child.draw(canvas, shadow)
    
    def is_resizable(self):
        ret_x, ret_y = True, True
        def_x, def_y = self._get_default_resizable()
        
        for child in self.__children:
            child_x, child_y = child.child.is_resizable()
            
            ret_x = ret_x and child_x
            ret_y = ret_y and child_y
        
        return def_x or ret_x, def_y or ret_y


class BoxComponent(VisualComponent):
    CHILDREN_ATTRIBUTES = {
        'expand': UflBoolType(),
    }
    
    def __init__(self, object_type, children, expand):
        super().__init__(children)
        self.__object_type = object_type
        self.__expand = expand
    
    def _create_object(self, context, ruler):
        children = [
            BoxChild(child._create_object(local, ruler), self.__expand.get(child, False))
                for local, child in self._get_children(context)
        ]
        
        return self.__object_type(children)
    
    def compile(self, variables):
        self._compile_children(variables)
