from itertools import chain
from uuid import uuid4
from weakref import ref
from umlfri2.types.geometry import Rectangle
from umlfri2.ufl.dialog import UflDialog, UflDialogOptions
from .connection import ConnectionObject, ConnectionVisual
from .element import ElementObject, ElementVisual
from umlfri2.ufl.types.uniquevaluegenerator import UniqueValueGenerator


class DiagramValueGenerator(UniqueValueGenerator):
    def __init__(self, parent, type):
        self.__parent = parent
        self.__type = type
        self.__name = None
    
    def get_parent_name(self):
        return self.__parent.get_display_name()
    
    def for_name(self, name):
        ret = DiagramValueGenerator(self.__parent, self.__type)
        ret.__name = name
        return ret
    
    def has_value(self, value):
        if self.__name is None:
            return None
        
        for diagram in self.__parent.diagrams:
            if diagram.type == self.__type and diagram.data.get_value(self.__name) == value:
                return True
        
        return False


class Diagram:
    def __init__(self, parent, type, save_id=None):
        self.__parent = ref(parent)
        self.__type = type
        self.__data = type.ufl_type.build_default(DiagramValueGenerator(parent, type))
        self.__elements = []
        self.__connections = []
        if save_id is None:
            self.__save_id = uuid4()
        else:
            self.__save_id = save_id
    
    @property
    def parent(self):
        return self.__parent()
    
    def change_parent(self, new_parent, new_index):
        if self.project is not new_parent.project:
            raise Exception
        
        self.__parent().remove_child(self)
        self.__parent = ref(new_parent)
        self.__parent().add_child(self, new_index)
    
    @property
    def project(self):
        return self.__parent().project
    
    @property
    def type(self):
        return self.__type
    
    @property
    def data(self):
        return self.__data
    
    @property
    def elements(self):
        yield from self.__elements
    
    @property
    def element_count(self):
        return len(self.__elements)
    
    @property
    def connections(self):
        yield from self.__connections
    
    @property
    def save_id(self):
        return self.__save_id
    
    def get_display_name(self):
        return self.__type.get_display_name(self)
    
    def show(self, object):
        if isinstance(object, ElementObject):
            visual = ElementVisual(self, object)
            self.__elements.append(visual)
            object.add_visual(visual)
            return visual
        elif isinstance(object, ConnectionObject):
            element1 = None
            element2 = None
            for element in self.__elements:
                if element.object is object.source:
                    element1 = element
                if element.object is object.destination:
                    element2 = element
            
            if element1 is not None and element2 is not None:
                visual = ConnectionVisual(self, object, element1, element2)
                element1.add_connection(visual)
                element2.add_connection(visual)
                self.__connections.append(visual)
                object.add_visual(visual)
                return visual
        else:
            raise Exception
    
    def add(self, visual, z_order=None):
        if visual.diagram is not self:
            raise Exception
        
        if isinstance(visual, ElementVisual):
            if visual in self.__elements:
                raise Exception
            
            if z_order is None:
                self.__elements.append(visual)
            else:
                self.__elements.insert(z_order, visual)
            
            visual.object.add_visual(visual)
        elif isinstance(visual, ConnectionVisual):
            if visual in self.__connections:
                raise Exception
            
            if z_order is None:
                self.__connections.append(visual)
            else:
                self.__connections.insert(z_order, visual)
            
            visual.source.add_connection(visual)
            visual.destination.add_connection(visual)
            
            visual.object.add_visual(visual)
        else:
            raise Exception
    
    def remove(self, visual):
        if visual.diagram is not self:
            raise Exception
        
        if isinstance(visual, ElementVisual):
            if visual not in self.__elements:
                raise Exception
            for connection in visual.connections:
                if connection in self.__connections:
                    raise Exception
            self.__elements.remove(visual)
            
            visual.object.remove_visual(visual)
        elif isinstance(visual, ConnectionVisual):
            if visual not in self.__connections:
                raise Exception
            self.__connections.remove(visual)
            visual.source.remove_connection(visual)
            visual.destination.remove_connection(visual)
            
            visual.object.remove_visual(visual)
        else:
            raise Exception
    
    def get_z_order(self, visual):
        if visual.diagram is not self:
            raise Exception
        
        if isinstance(visual, ElementVisual):
            return self.__elements.index(visual)
        elif isinstance(visual, ConnectionVisual):
            return self.__connections.index(visual)
        else:
            raise Exception
    
    def change_z_order(self, visual, z_order):
        if visual.diagram is not self:
            raise Exception
        
        if isinstance(visual, ElementVisual):
            self.__elements.remove(visual)
            self.__elements.insert(z_order, visual)
        elif isinstance(visual, ConnectionVisual):
            self.__connections.remove(visual)
            self.__connections.insert(z_order, visual)
        else:
            raise Exception
    
    def change_z_order_many(self, z_order_visuals):
        for z_order, visual in z_order_visuals:
            if not isinstance(visual, (ElementVisual, ConnectionVisual)):
                raise Exception
            if visual.diagram is not self:
                raise Exception
        
        for z_order, visual in z_order_visuals:
            if isinstance(visual, ElementVisual):
                self.__elements.remove(visual)
            else:
                self.__connections.remove(visual)
        
        for z_order, visual in z_order_visuals:
            if isinstance(visual, ElementVisual):
                self.__elements.insert(z_order, visual)
            else:
                self.__connections.insert(z_order, visual)
    
    def draw_background(self, canvas):
        canvas.clear(self.__type.get_background_color(self))
    
    def draw(self, canvas, selection=None, transparent=False):
        if not transparent:
            self.draw_background(canvas)
        
        for element in self.__elements:
            element.draw(canvas)
            if selection is not None:
                selection.draw_for(canvas, element)
        
        for connection in self.__connections:
            connection.draw(canvas)
            if selection is not None:
                selection.draw_for(canvas, connection)
    
    def get_visual_for(self, object):
        for visual in chain(self.__elements, self.__connections):
            if visual.object is object:
                return visual
        return None
    
    def get_visual_at(self, ruler, position):
        for connection in reversed(self.__connections):
            if connection.is_at_position(ruler, position):
                return connection
        
        for element in reversed(self.__elements):
            if element.is_at_position(ruler, position):
                return element
        
        return None
    
    def get_visual_above(self, ruler, visual, skip=set()):
        # TODO: implement it for connections too
        element_bounds = visual.get_bounds(ruler)
        
        above_visual = None
        for current_element in reversed(self.__elements):
            if current_element is visual:
                return above_visual
            elif current_element.get_bounds(ruler).is_overlapping(element_bounds):
                if current_element not in skip:
                    above_visual = current_element
        
        raise Exception
    
    def get_visual_below(self, ruler, visual, skip=set()):
        # TODO: implement it for connections too
        element_bounds = visual.get_bounds(ruler)
        
        above_visual = None
        for current_element in self.__elements:
            if current_element is visual:
                return above_visual
            elif current_element.get_bounds(ruler).is_overlapping(element_bounds):
                if current_element not in skip:
                    above_visual = current_element
        
        raise Exception
    
    def get_size(self, ruler):
        return self.get_bounds(ruler).bottom_right.as_size()
    
    def get_bounds(self, ruler):
        return Rectangle.combine_bounds(visual.get_bounds(ruler)
                                        for visual in chain(self.__elements, self.__connections))
    
    def contains(self, object):
        if isinstance(object, ElementObject):
            for visual in self.__elements:
                if visual.object is object:
                    return True
        elif isinstance(object, ElementVisual):
            for visual in self.__elements:
                if visual is object:
                    return True
        elif isinstance(object, ConnectionObject):
            for visual in self.__connections:
                if visual.object is object:
                    return True
        elif isinstance(object, ConnectionVisual):
            for visual in self.__connections:
                if visual is object:
                    return True
    
    def apply_ufl_patch(self, patch):
        self.__data.apply_patch(patch)
    
    @property
    def has_ufl_dialog(self):
        return self.__type.ufl_type.has_attributes
    
    def create_ufl_dialog(self, options=UflDialogOptions.standard):
        if not self.__type.ufl_type.has_attributes:
            raise Exception
        dialog = UflDialog(self.__type.ufl_type, options)
        dialog.associate(self.__data)
        return dialog
