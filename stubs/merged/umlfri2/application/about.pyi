from .updates import UmlFriUpdates as UmlFriUpdates
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.types.version import Version as Version
from typing import (
    Iterator,
    Tuple,
)
from umlfri2.application.application import Application
from umlfri2.application.updates import UmlFriUpdates


class AboutUmlFri:
    name: str
    version: Incomplete
    is_debug_version = __debug__
    def __init__(self, application: Application) -> None: ...
    @property
    def urls(self) -> Iterator[str]: ...
    @property
    def author(self) -> Iterator[Tuple[str, Tuple[int, int]]]: ...
    @property
    def description(self) -> str: ...
    @property
    def dependency_versions(self) -> Iterator[Tuple[str, str]]: ...
    @property
    def version_1_contributions(self) -> Iterator[Tuple[str, Tuple[int, int]]]: ...
    @property
    def updates(self) -> UmlFriUpdates: ...
