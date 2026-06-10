from typing import (
    Optional,
    Union,
)
from umlfri2.metamodel.metamodel import Metamodel
from umlfri2.ufl.types.structured.object import (
    UflObjectAttribute,
    UflObjectType,
)


class ConfigAttributeTranslation:
    def translate(
        self,
        object: Union[Metamodel, UflObjectType, UflObjectAttribute]
    ) -> Optional[str]: ...
