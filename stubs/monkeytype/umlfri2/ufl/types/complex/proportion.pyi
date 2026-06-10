from typing import Optional
from umlfri2.types.proportion import Proportion


class UflProportionType:
    def __init__(self, default: None = ...) -> None: ...
    def parse(self, value: str) -> Proportion: ...
