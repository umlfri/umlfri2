from typing import Union


class MaybeType:
    def __and__(
        self,
        other: Union[MaybeType, bool]
    ) -> Union[MaybeType, bool]: ...
    def __or__(self, other: bool) -> Union[MaybeType, bool]: ...
    def __rand__(self, other: bool) -> bool: ...
