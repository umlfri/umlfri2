from typing import (
    Any,
    Dict,
    List,
)
from umlfri2.metamodel.diagramtype import DiagramType
from umlfri2.metamodel.metamodel import Metamodel


class DiagramTemplate:
    def __init__(
        self,
        type: str,
        data: Dict[Any, Any],
        elements: List[Any],
        connections: List[Any],
        parent_id: int,
        state: DiagramTemplateState = ...
    ) -> None: ...
    def _compile(self, metamodel: Metamodel) -> None: ...
    @property
    def connections(self) -> None: ...
    @property
    def data(self) -> Dict[Any, Any]: ...
    @property
    def elements(self) -> None: ...
    @property
    def parent_id(self) -> int: ...
    @property
    def state(self) -> DiagramTemplateState: ...
    @property
    def type(self) -> DiagramType: ...
