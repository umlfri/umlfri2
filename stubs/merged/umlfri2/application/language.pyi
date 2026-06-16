from .events.application import LanguageChangedEvent as LanguageChangedEvent
from umlfri2.constants.paths import LOCALE_DIR as LOCALE_DIR
from typing import Optional
from umlfri2.application.application import Application


class LanguageManager:
    def __init__(self, application: Application) -> None: ...
    def change_language(self, language: Optional[str]) -> None: ...
    @property
    def current_language(self) -> str: ...
