from typing import (
    List,
    Union,
)
from umlfri2.ufl.types.basic.bool import UflBoolType
from umlfri2.ufl.types.generic.anycomparable import UflAnyComparableType
from umlfri2.ufl.types.generic.generic import UflGenericType
from umlfri2.ufl.types.structured.object import UflObjectType


class UflLambdaType:
    def __init__(
        self,
        parameter_types: List[Union[UflObjectType, UflGenericType]],
        return_type: Union[UflAnyComparableType, UflGenericType, UflBoolType]
    ) -> None: ...
    @property
    def parameter_count(self) -> int: ...
    @property
    def return_type(self) -> UflBoolType: ...
