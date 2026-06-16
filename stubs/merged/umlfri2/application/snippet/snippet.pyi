from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.types.geometry import Point as Point, Size as Size
from umlfri2.ufl.types.complex import UflColorType as UflColorType, UflFontType as UflFontType, UflImageType as UflImageType, UflProportionType as UflProportionType
from umlfri2.ufl.types.structured import UflListType as UflListType, UflObjectType as UflObjectType
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
    def serialize(self) -> str: ...
    @staticmethod
    def deserialize(data: str) -> Snippet: ...
    @property
    def empty(self) -> bool: ...
    def can_be_pasted_to(self, diagram: Diagram) -> bool: ...
    def paste_to(self, ruler, diagram) -> Generator[Incomplete]: ...
    def can_be_duplicated_to(self, diagram: Diagram) -> bool: ...
    def duplicate_to(
        self,
        ruler: QTRuler,
        diagram: Diagram
    ) -> Iterator[Union[ElementVisual, ConnectionVisual]]: ...
