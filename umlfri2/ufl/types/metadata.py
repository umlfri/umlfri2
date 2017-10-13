from .type import UflType


class UflMetadataType(UflType):
    def __init__(self, metadata_type):
        metadata = {}
        for name, type in metadata_type.items():
            metadata[name] = (name, type)

        self.ALLOWED_DIRECT_ATTRIBUTES = metadata
    
    @property
    def is_immutable(self):
        return True
    
    def __str__(self):
        return "[Metadata {0}]".format(", ".join(self.ALLOWED_DIRECT_ATTRIBUTES.keys()))


class UflDataWithMetadataType(UflType):
    def __init__(self, underlying_type, **metadata_types):
        self.__underlying_type = underlying_type
        self.__metadata_types = metadata_types
    
    @property
    def underlying_type(self):
        return self.__underlying_type
    
    @property
    def metadata_type(self):
        return UflMetadataType(self.__metadata_types)
    
    def __str__(self):
        return "[DataWithMetadata {0} {1}]".format(repr(self.__underlying_type), ", ".join(self.__metadata_types.keys()))
