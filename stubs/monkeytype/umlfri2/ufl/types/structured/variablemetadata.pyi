from typing import (
    Dict,
    Iterator,
    Tuple,
    Union,
)
from umlfri2.ufl.types.basic.bool import UflBoolType
from umlfri2.ufl.types.basic.integer import UflIntegerType
from umlfri2.ufl.types.basic.string import UflStringType
from umlfri2.ufl.types.complex.image import UflImageType
from umlfri2.ufl.types.generic.any import UflAnyType
from umlfri2.ufl.types.structured.iterable import UflIterableType
from umlfri2.ufl.types.structured.object import UflObjectType


class UflVariableMetadataType:
    def __init__(
        self,
        metadata_type: Dict[str, Union[UflImageType, UflStringType, UflIterableType, UflIntegerType, UflBoolType]],
        underlying_type: Union[UflObjectType, UflVariableWithMetadataType]
    ) -> None: ...


class UflVariableWithMetadataType:
    def __init__(
        self,
        underlying_type: Union[UflObjectType, UflAnyType, UflVariableWithMetadataType],
        **metadata_types
    ) -> None: ...
    def _add_metadata_type(self, name: str, type: UflIterableType) -> None: ...
    @property
    def metadata_type(self) -> UflVariableMetadataType: ...
    @property
    def metadata_types(
        self
    ) -> Iterator[Union[Tuple[str, UflImageType], Tuple[str, UflStringType], Tuple[str, UflIterableType]]]: ...
    @property
    def underlying_type(
        self
    ) -> Union[UflAnyType, UflObjectType]: ...
