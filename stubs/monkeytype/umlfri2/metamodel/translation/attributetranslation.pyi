from typing import (
    Any,
    Optional,
    Union,
)
from umlfri2.metamodel.translation.configattributetransslation import ConfigAttributeTranslation


class AttributeTranslation:
    def __init__(self, multi: bool = ...) -> None: ...
    def add_parent(
        self,
        name: str
    ) -> Union[AttributeTranslation, ConfigAttributeTranslation]: ...
    @property
    def has_parents(self) -> bool: ...
    def translate(self, object: Any) -> Optional[str]: ...
