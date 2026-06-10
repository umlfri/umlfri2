from typing import (
    Any,
    Dict,
    List,
    Optional,
)
from umlfri2.metamodel.elementtype import ElementType
from umlfri2.metamodel.metamodel import Metamodel


class ElementTemplate:
    def __init__(self, type: str, data: Dict[str, str], children: List[Any], id: Optional[int] = ...) -> None: ...
    def _compile(self, metamodel: Metamodel) -> None: ...
    @property
    def children(self) -> None: ...
    @property
    def data(self) -> Dict[str, str]: ...
    @property
    def id(self) -> int: ...
    @property
    def type(self) -> ElementType: ...
