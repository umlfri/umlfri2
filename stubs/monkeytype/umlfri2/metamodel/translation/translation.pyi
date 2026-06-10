from typing import (
    Any,
    List,
    Tuple,
    Union,
)


class Translation:
    def __init__(self, language: str, translations: Union[List[Tuple[str, str, str]], Tuple[()]]) -> None: ...
    @property
    def language(self) -> str: ...
    def translate(self, object: Any) -> str: ...
