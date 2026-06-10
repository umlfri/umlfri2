from typing import Optional
from umlfri2.application.about import AboutUmlFri
from umlfri2.application.application import Application
from umlfri2.types.version import Version


class UmlFriUpdate:
    @property
    def is_newer(self) -> bool: ...
    @property
    def version(self) -> Version: ...


class UmlFriUpdates:
    def __init__(
        self,
        about: AboutUmlFri,
        application: Application
    ) -> None: ...
    @property
    def checking_update(self) -> bool: ...
    @property
    def has_error(self) -> bool: ...
    @property
    def latest_prerelease(self) -> None: ...
    @property
    def latest_version(self) -> Optional[UmlFriUpdate]: ...
    def recheck_update(self) -> None: ...
