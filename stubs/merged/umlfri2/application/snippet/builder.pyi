from .snippet import Snippet as Snippet
from umlfri2.ufl.types.complex import UflColorType as UflColorType, UflFontType as UflFontType, UflImageType as UflImageType, UflProportionType as UflProportionType
from umlfri2.ufl.types.enum import UflFlagsType as UflFlagsType
from umlfri2.ufl.types.structured import UflListType as UflListType, UflNullableType as UflNullableType, UflObjectType as UflObjectType
from umlfri2.application.snippet.snippet import Snippet
from umlfri2.model.connection.connectionvisual import ConnectionVisual
from umlfri2.model.element.elementvisual import ElementVisual
from umlfri2.model.project import Project
from umlfri2.qtgui.rendering.qtruler import QTRuler


class SnippetBuilder:
    def __init__(self, project: Project) -> None: ...
    def add_element(
        self,
        ruler: QTRuler,
        visual: ElementVisual
    ) -> SnippetBuilder: ...
    def add_connection(
        self,
        ruler: QTRuler,
        visual: ConnectionVisual
    ) -> SnippetBuilder: ...
    def build(self) -> Snippet: ...
