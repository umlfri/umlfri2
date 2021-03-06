from collections import namedtuple

from umlfri2.types.geometry import Size, Rectangle
from umlfri2.types.threestate import Maybe
from umlfri2.ufl.types.basic import UflBoolType
from .empty import EmptyObject
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

    def _combine_resizable(self, ret_x, ret_y, child_x, child_y, expand):
        raise NotImplemented
    
    def assign_bounds(self, bounds):
        position = bounds.top_left
        whole_size = bounds.size
        
        if self.__children:
            deltas = self.__compute_deltas(
                [self._get_size_component(size) for size in self.__children_sizes],
                self._get_size_component(whole_size)
            )
            for size, delta, child in zip(self.__children_sizes, deltas, self.__children):
                new_size = self._new_size(size, whole_size, delta)
                child.child.assign_bounds(Rectangle.from_point_size(position, new_size))
                position = self._new_position(position, new_size)
    
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
        ret_x = Maybe
        ret_y = Maybe
        
        for child in self.__children:
            child_x, child_y = child.child.is_resizable()
            
            ret_x, ret_y = self._combine_resizable(ret_x, ret_y, child_x, child_y, child.expand)
        
        return ret_x, ret_y


class BoxComponent(VisualComponent):
    CHILDREN_ATTRIBUTES = {
        'expand': UflBoolType(),
    }
    
    def __init__(self, object_type, children, expand):
        super().__init__(children)
        self.__object_type = object_type
        self.__expand = expand
    
    def _create_object(self, context, ruler):
        children = []

        for local, child in self._get_children(context):
            child_object = child._create_object(local, ruler)
            if child in self.__expand:
                child_expand = self.__expand[child](local)
            else:
                child_expand = False
            children.append(BoxChild(child_object, child_expand))
        
        if children:
            return self.__object_type(children)
        else:
            return EmptyObject()
    
    def compile(self, type_context):
        self._compile_child_expressions(
            type_context,
            expand=self.__expand
        )
        
        self._compile_children(type_context)
