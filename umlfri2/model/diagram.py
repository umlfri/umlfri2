from __future__ import annotations

from itertools import chain
from typing import Any, Iterable, Iterator, List, Optional, Set, Tuple, TYPE_CHECKING, Union
from uuid import UUID, uuid4
from weakref import ref

from umlfri2.types.geometry import Rectangle, Size, Point
from umlfri2.ufl.dialog import UflDialog, UflDialogOptions
from umlfri2.ufl.uniquevaluegenerator import UniqueValueGenerator
from .connection import ConnectionObject, ConnectionVisual
from .element import ElementObject, ElementVisual

if TYPE_CHECKING:
    from umlfri2.metamodel.diagramtype import DiagramType
    from umlfri2.model import Project
    from umlfri2.types.color import Color
    from umlfri2.ufl.objects import UflObject, UflObjectPatch


class DiagramValueGenerator(UniqueValueGenerator):
    def __init__(self, parent: ElementObject, type: DiagramType) -> None:
        self.__parent = parent
        self.__type = type
        self.__name: Optional[str] = None
    
    def get_parent_name(self) -> str:
        return self.__parent.get_display_name()
    
    def for_name(self, name: str) -> DiagramValueGenerator:
        ret = DiagramValueGenerator(self.__parent, self.__type)
        ret.__name = name
        return ret
    
    def has_value(self, value: Any) -> Optional[bool]:
        if self.__name is None:
            return None
        
        for diagram in self.__parent.diagrams:
            if diagram.type == self.__type and diagram.data.get_value(self.__name) == value:
                return True
        
        return False


class Diagram:
    def __init__(self, parent: ElementObject, type: DiagramType, save_id: Optional[UUID] = None) -> None:
        self.__parent = ref(parent)
        self.__type = type
        self.__data = type.ufl_type.build_default(DiagramValueGenerator(parent, type))
        self.__elements: List[ElementVisual] = []
        self.__connections: List[ConnectionVisual] = []
        if save_id is None:
            self.__save_id = uuid4()
        else:
            self.__save_id = save_id
    
    @property
    def parent(self) -> ElementObject:
        return self.__parent()
    
    def change_parent(self, new_parent: ElementObject, new_index: int) -> None:
        if self.project is not new_parent.project:
            raise Exception
        
        self.__parent().remove_child(self)
        self.__parent = ref(new_parent)
        self.__parent().add_child(self, new_index)
    
    @property
    def project(self) -> Project:
        return self.__parent().project
    
    @property
    def type(self) -> DiagramType:
        return self.__type
    
    @property
    def data(self) -> UflObject:
        return self.__data
    
    @property
    def elements(self) -> Iterator[ElementVisual]:
        yield from self.__elements
    
    @property
    def element_count(self) -> int:
        return len(self.__elements)
    
    @property
    def connections(self) -> Iterator[ConnectionVisual]:
        yield from self.__connections
    
    @property
    def save_id(self) -> UUID:
        return self.__save_id
    
    def get_display_name(self) -> str:
        return self.__type.get_display_name(self)
    
    def show(self, object: Union[ElementObject, ConnectionObject]) -> Union[ElementVisual, ConnectionVisual]:
        if isinstance(object, ElementObject):
            visual = ElementVisual(self, object)
            self.__elements.append(visual)
            object.add_visual(visual)
            return visual
        elif isinstance(object, ConnectionObject):
            element1: Optional[ElementVisual] = None
            element2: Optional[ElementVisual] = None
            for element in self.__elements:
                if element.object is object.source:
                    element1 = element
                if element.object is object.destination:
                    element2 = element
            
            if element1 is not None and element2 is not None:
                visual = ConnectionVisual(self, object, element1, element2)
                element1.add_connection(visual)
                if element1 is not element2:
                    element2.add_connection(visual)
                self.__connections.append(visual)
                object.add_visual(visual)
                return visual
            else:
                raise Exception
        else:
            raise Exception
    
    def add(self, visual: Union[ElementVisual, ConnectionVisual], z_order: Optional[int] = None) -> None:
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
            if visual.source is not visual.destination:
                visual.destination.add_connection(visual)
            
            visual.object.add_visual(visual)
        else:
            raise Exception
    
    def remove(self, visual: Union[ElementVisual, ConnectionVisual]) -> None:
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
            if visual.source is not visual.destination:
                visual.destination.remove_connection(visual)
            
            visual.object.remove_visual(visual)
        else:
            raise Exception
    
    def get_z_order(self, visual: Union[ElementVisual, ConnectionVisual]) -> int:
        if visual.diagram is not self:
            raise Exception
        
        if isinstance(visual, ElementVisual):
            return self.__elements.index(visual)
        elif isinstance(visual, ConnectionVisual):
            return self.__connections.index(visual)
        else:
            raise Exception
    
    def change_z_order(self, visual: Union[ElementVisual, ConnectionVisual], z_order: int) -> None:
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
    
    def change_z_order_many(self, z_order_visuals: Iterable[Tuple[int, Union[ElementVisual, ConnectionVisual]]]) -> None:
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
    
    def draw_background(self, canvas: object) -> None:
        canvas.clear(self.__type.get_background_color(self))
    
    def draw(self, canvas: object, selection: object = None, transparent: bool = False) -> None:
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
    
    def get_visual_for(self, object: Union[ElementObject, ConnectionObject]) -> Optional[Union[ElementVisual, ConnectionVisual]]:
        for visual in chain(self.__elements, self.__connections):
            if visual.object is object:
                return visual
        return None
    
    def get_visual_at(self, ruler: object, position: Point) -> Optional[Union[ElementVisual, ConnectionVisual]]:
        for connection in reversed(self.__connections):
            if connection.is_at_position(ruler, position):
                return connection
        
        for element in reversed(self.__elements):
            if element.is_at_position(ruler, position):
                return element
        
        return None
    
    def get_visual_above(self, ruler: object, visual: ElementVisual,
                         skip: Set[ElementVisual] = set()) -> Optional[ElementVisual]:
        element_bounds = visual.get_bounds(ruler)
        
        above_visual: Optional[ElementVisual] = None
        for current_element in reversed(self.__elements):
            if current_element is visual:
                return above_visual
            elif current_element.get_bounds(ruler).is_overlapping(element_bounds):
                if current_element not in skip:
                    above_visual = current_element
        
        raise Exception
    
    def get_visual_below(self, ruler: object, visual: ElementVisual,
                         skip: Set[ElementVisual] = set()) -> Optional[ElementVisual]:
        element_bounds = visual.get_bounds(ruler)
        
        above_visual: Optional[ElementVisual] = None
        for current_element in self.__elements:
            if current_element is visual:
                return above_visual
            elif current_element.get_bounds(ruler).is_overlapping(element_bounds):
                if current_element not in skip:
                    above_visual = current_element
        
        raise Exception
    
    def get_size(self, ruler: object) -> Size:
        return self.get_bounds(ruler).bottom_right.as_size()
    
    def get_bounds(self, ruler: object) -> Rectangle:
        return Rectangle.combine_bounds(visual.get_bounds(ruler)
                                        for visual in chain(self.__elements, self.__connections))
    
    def contains(self, object: Union[ElementObject, ElementVisual, ConnectionObject, ConnectionVisual]) -> bool:
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
        
        return False
    
    def apply_ufl_patch(self, patch: UflObjectPatch) -> None:
        self.__data.apply_patch(patch)
    
    @property
    def has_ufl_dialog(self) -> bool:
        return self.__type.ufl_type.has_attributes
    
    def create_ufl_dialog(self, options: UflDialogOptions = UflDialogOptions.standard) -> UflDialog:
        if not self.__type.ufl_type.has_attributes:
            raise Exception
        dialog = UflDialog(self.__type.ufl_type, options)
        dialog.associate(self.__data)
        return dialog
