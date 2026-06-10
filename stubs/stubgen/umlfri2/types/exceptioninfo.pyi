from _typeshed import Incomplete
from collections.abc import Generator
from typing import NamedTuple
from umlfri2.constants.paths import ROOT_DIR as ROOT_DIR

class ExceptionInfoLine(NamedTuple):
    filename: Incomplete
    module: Incomplete
    lineno: Incomplete
    function: Incomplete
    text: Incomplete

class ExceptionInfo:
    def __init__(self, type_name, description, traceback, cause=None, context=None) -> None: ...
    @staticmethod
    def from_exception(exception): ...
    @property
    def type_name(self): ...
    @property
    def description(self): ...
    @property
    def traceback(self) -> Generator[Incomplete, Incomplete]: ...
    @property
    def cause(self): ...
    @property
    def context(self): ...
