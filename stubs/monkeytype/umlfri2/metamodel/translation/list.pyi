from typing import (
    Any,
    List,
    Union,
)
from umlfri2.metamodel.translation.translation import Translation


class TranslationList:
    def __init__(self, translations: List[Union[Any, Translation]]) -> None: ...
    def get_translation(self, language: str) -> Translation: ...
