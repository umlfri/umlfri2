from typing import (
    Dict,
    Iterator,
    List,
    Tuple,
    Union,
)
from umlfri2.model.connection.connectionvisual import ConnectionVisual
from umlfri2.model.diagram import Diagram
from umlfri2.model.element.elementvisual import ElementVisual
from umlfri2.qtgui.rendering.qtruler import QTRuler


class Snippet:
    def __init__(
        self,
        data: Dict[str, Union[str, Tuple[Dict[str, Union[str, int, Dict[str, str]]], Dict[str, Union[str, int, Dict[str, str]]], Dict[str, Union[str, int, Dict[str, str]]], Dict[str, Union[str, int, Dict[str, str]]]], Tuple[Dict[str, Union[str, int, Dict[str, str]]], Dict[str, Union[str, int, Dict[str, str]]], Dict[str, Union[str, Dict[str, Dict[str, int]], Dict[str, str]]]], List[Dict[str, Union[str, int, Dict[str, str]]]]]]
    ) -> None: ...
    def can_be_duplicated_to(self, diagram: Diagram) -> bool: ...
    def can_be_pasted_to(self, diagram: Diagram) -> bool: ...
    @staticmethod
    def deserialize(data: str) -> Snippet: ...
    def duplicate_to(
        self,
        ruler: QTRuler,
        diagram: Diagram
    ) -> Iterator[Union[ElementVisual, ConnectionVisual]]: ...
    @property
    def empty(self) -> bool: ...
    def serialize(self) -> str: ...
