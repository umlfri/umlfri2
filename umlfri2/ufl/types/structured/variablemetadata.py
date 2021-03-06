from ..base.type import UflType, UflAttributeDescription


class UflVariableMetadataType(UflType):
    def __init__(self, metadata_type, underlying_type):
        metadata = {}
        for name, type in metadata_type.items():
            metadata[name] = UflAttributeDescription(name, type)
        
        next_type = underlying_type
        next_prefix = '{0}.'.format(UflVariableWithMetadataType.VALUE_ATTRIBUTE)
        
        while isinstance(next_type, UflVariableWithMetadataType):
            for name, type in next_type.metadata_types:
                if name not in metadata:
                    metadata[name] = UflAttributeDescription(next_prefix + name, type)
            next_type = next_type.underlying_type
            next_prefix = '{0}.{1}'.format(UflVariableWithMetadataType.VALUE_ATTRIBUTE, next_prefix)

        self.ALLOWED_DIRECT_ATTRIBUTES = metadata
    
    @property
    def is_immutable(self):
        return True
    
    def __str__(self):
        return "[VariableMetadata {0}]".format(", ".join(self.ALLOWED_DIRECT_ATTRIBUTES.keys()))


class UflVariableWithMetadataType(UflType):
    VALUE_ATTRIBUTE = 'value'
    
    def __init__(self, underlying_type, **metadata_types):
        self.__underlying_type = underlying_type
        self.__metadata_types = metadata_types
    
    # use with caution, only for recursive metadata
    def _add_metadata_type(self, name, type):
        self.__metadata_types[name] = type
    
    @property
    def metadata_types(self):
        yield from self.__metadata_types.items()
    
    @property
    def underlying_type(self):
        return self.__underlying_type
    
    @property
    def metadata_type(self):
        return UflVariableMetadataType(self.__metadata_types, self.__underlying_type)
    
    def is_equatable_to(self, other):
        if isinstance(other, UflVariableWithMetadataType):
            return self.__underlying_type.is_equatable_to(other.__underlying_type)
        else:
            return self.__underlying_type.is_equatable_to(other)
    
    def is_comparable_with(self, other):
        if isinstance(other, UflVariableWithMetadataType):
            return self.__underlying_type.is_comparable_with(other.__underlying_type)
        else:
            return self.__underlying_type.is_comparable_with(other)
    
    def is_convertible_to(self, other):
        return self.__underlying_type.is_convertible_to(other)
    
    def resolve_unknown_generic(self, generics_cache):
        raise Exception("Generic variable metadata is a nonsense, sorry.")
    
    def resolve_generic(self, actual_type, generics_cache):
        raise Exception("Generic variable metadata is a nonsense, sorry.")
    
    def __str__(self):
        return "[VariableWithMetadata {0} {1}]".format(repr(self.__underlying_type), ", ".join(self.__metadata_types.keys()))
