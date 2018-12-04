from collections import namedtuple
from weakref import ref

from umlfri2.ufl.context import Context
from umlfri2.ufl.types import UflVariableWithMetadataType, UflStringType, UflImageType, UflAnyType, UflIterableType

ElementAccessDepth = namedtuple('ElementAccessDepth', ('parent', 'child'))


class NodeMetadata:
    def __init__(self, element, node_access_depth):
        self.__element = element
        self.__node_access_depth = node_access_depth
    
    @property
    def children(self):
        if self.__node_access_depth.child > 0:
            child_access_depth = ElementAccessDepth(self.__node_access_depth.parent + 1, self.__node_access_depth.child - 1)
            for child in self.__element.children:
                yield NodeMetadata(child, child_access_depth)
    
    @property
    def icon(self):
        return self.__element.type.icon
    
    @property
    def label(self):
        return self.__element.get_display_name()
    
    @property
    def value(self):
        return self.__element.data
    
    @staticmethod
    def build_node_metadata_types(element_type=None):
        metadata = {
            'icon': UflImageType(),
            'label': UflStringType(),
        }
        
        if element_type is None:
            ret = UflVariableWithMetadataType(UflAnyType(), **metadata)
            ret._add_metadata_type('children', UflIterableType(ret))
        else:
            ret = UflVariableWithMetadataType(element_type.ufl_type, **metadata)
            ret._add_metadata_type('children', UflIterableType(NodeMetadata.build_node_metadata_types(None)))
        
        return ret


class ElementType:
    def __init__(self, id, icon, ufl_type, display_name, appearance, default_action, node_access_depth,
                 allow_direct_add):
        self.__metamodel = None
        self.__id = id
        self.__icon = icon
        self.__ufl_type = ufl_type
        self.__ufl_type.set_parent(self)
        self.__display_name = display_name
        self.__appearance = appearance
        self.__default_action = default_action
        self.__node_access_depth = node_access_depth
        self.__allow_direct_add = allow_direct_add
    
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
    
    @property
    def allow_direct_add(self):
        return self.__allow_direct_add
    
    def compile(self, type_context):
        type_context = type_context \
            .set_variable_type('self', self.__ufl_type) \
            .set_variable_type('cfg', self.__metamodel().config_structure)

        appearance_type_context = type_context
        
        if self.__node_access_depth.child > 0 or self.__node_access_depth.parent > 0:
            appearance_type_context = appearance_type_context \
                .set_variable_type('self', NodeMetadata.build_node_metadata_types(self))
        
        self.__appearance.compile(appearance_type_context)
        
        self.__display_name.compile(type_context)
    
    def create_appearance_object(self, element, ruler):
        if self.__node_access_depth.child > 0 or self.__node_access_depth.parent > 0:
            data = NodeMetadata(element, self.__node_access_depth)
        else:
            data = element.data
        
        context = Context()\
            .set_variable('self', data)\
            .set_variable('cfg', element.project.config)
        return self.__appearance.create_visual_object(context, ruler)
    
    def get_display_name(self, element):
        context = Context()\
            .set_variable('self', element.data)\
            .set_variable('cfg', element.project.config)
        return self.__display_name.get_text(context)
