from collections import namedtuple
from weakref import ref

from umlfri2.components.base.context import Context
from umlfri2.ufl.types import UflType, UflListType, UflImageType, UflStringType, UflIterableType


class UflNodeType(UflType):
    def __init__(self, node_access_depth):
        allowed_attributes = {
            'icon': ('icon', UflImageType()),
            'label': ('label', UflStringType()),
        }
        
        if node_access_depth.child > 0:
            deeper_node_access_depth = ElementAccessDepth(node_access_depth.parent + 1, node_access_depth.child - 1)
            allowed_attributes['children'] = ('children', UflIterableType(UflNodeType(deeper_node_access_depth)))
        
        self.ALLOWED_DIRECT_ATTRIBUTES = allowed_attributes


class UflNode:
    def __init__(self, element):
        self.__element = element
    
    @property
    def children(self):
        for child in self.__element.children:
            yield UflNode(child)
    
    @property
    def icon(self):
        return self.__element.type.icon
    
    @property
    def label(self):
        return self.__element.get_display_name()


ElementAccessDepth = namedtuple('ElementAccessDepth', ('parent', 'child'))


class ElementType:
    def __init__(self, id, icon, ufl_type, display_name, appearance, default_action, node_access_depth):
        self.__metamodel = None
        self.__id = id
        self.__icon = icon
        self.__ufl_type = ufl_type
        self.__ufl_type.set_parent(self)
        self.__display_name = display_name
        self.__appearance = appearance
        self.__default_action = default_action
        self.__node_access_depth = node_access_depth
    
    def _set_metamodel(self, metamodel):
        self.__metamodel = ref(metamodel)
    
    @property
    def metamodel(self):
        return self.__metamodel()
    
    @property
    def id(self):
        return self.__id
    
    @property
    def icon(self):
        return self.__icon
    
    @property
    def ufl_type(self):
        return self.__ufl_type
    
    @property
    def default_action(self):
        return self.__default_action
    
    @property
    def node_access_depth(self):
        return self.__node_access_depth
    
    def compile(self):
        variables = {
            'self': self.__ufl_type,
            'cfg': self.__metamodel().config_structure,
        }
        
        appearance_variables = variables.copy()
        appearance_variables.update(node=UflNodeType(self.__node_access_depth))
        
        self.__appearance.compile(appearance_variables)
        self.__display_name.compile(variables)
    
    def create_appearance_object(self, element, ruler):
        context = Context()\
            .extend(element.data, 'self')\
            .extend(self.__metamodel().config, 'cfg')\
            .extend(UflNode(element), 'node')
        return self.__appearance.create_visual_object(context, ruler)
    
    def get_display_name(self, element):
        context = Context()\
            .extend(element.data, 'self')\
            .extend(self.__metamodel().config, 'cfg')
        return self.__display_name.get_text(context)
