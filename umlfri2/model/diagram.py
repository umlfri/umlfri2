from itertools import chain
from uuid import uuid4
from weakref import ref
from umlfri2.components.base.context import Context
from umlfri2.types.geometry import Size, Rectangle
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
    def connections(self):
        yield from self.__connections
    
    @property
    def save_id(self):
        return self.__save_id
    
    def get_display_name(self):
        context = Context().extend(self.__data, 'self')
        return self.__type.get_display_name(context)
    
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
                return visual
        else:
            raise Exception
    
    def add(self, visual):
        if visual.diagram is not self:
            raise Exception
        
        if isinstance(visual, ElementVisual):
            if visual in self.__elements:
                raise Exception
            self.__elements.append(visual)
            visual.object.add_visual(visual)
            for connection in visual.connections:
                self.__connections.append(connection)
                connection.get_other_end(visual).add_connection(connection)
        elif isinstance(visual, ConnectionVisual):
            if visual in self.__connections:
                raise Exception
            self.__connections.append(visual)
            visual.source.add_connection(visual)
            visual.destination.add_connection(visual)
        else:
            raise Exception
    
    def remove(self, visual):
        if visual.diagram is not self:
            raise Exception
        
        if isinstance(visual, ElementVisual):
            if visual not in self.__elements:
                raise Exception
            self.__elements.remove(visual)
            visual.object.remove_visual(visual)
            for connection in visual.connections:
                self.__connections.remove(connection)
                connection.get_other_end(visual).remove_connection(connection)
        elif isinstance(visual, ConnectionVisual):
            if visual not in self.__connections:
                raise Exception
            self.__connections.remove(visual)
            visual.source.remove_connection(visual)
            visual.destination.remove_connection(visual)
        else:
            raise Exception
    
    def draw(self, canvas, selection=None):
        context = Context().extend(self.__data, 'self')
        canvas.clear(self.__type.get_background_color(context))
        
        for element in self.__elements:
            element.draw(canvas)
            if selection is not None:
                selection.draw_for(canvas, element)
        
        for connection in self.__connections:
            connection.draw(canvas)
            if selection is not None:
                selection.draw_for(canvas, connection)
    
    def get_visual_at(self, ruler, position):
        for connection in reversed(self.__connections):
            if connection.is_at_position(ruler, position):
                return connection
        
        for element in reversed(self.__elements):
            if element.is_at_position(ruler, position):
                return element
        
        return None
    
    def get_size(self, ruler):
        return Rectangle.combine_bounds(visual.get_bounds(ruler)
                                        for visual in chain(self.__elements, self.__connections)).bottom_right.as_size()
    
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
    
    def create_ufl_dialog(self, language, options=UflDialogOptions.standard):
        translation = self.type.metamodel.addon.get_translation(language)
        dialog = UflDialog(self.type.ufl_type, translation, options)
        dialog.associate(self.data)
        return dialog
