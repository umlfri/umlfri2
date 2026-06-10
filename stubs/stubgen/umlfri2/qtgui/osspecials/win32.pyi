from .base import OSSpecials as OSSpecials
from umlfri2.application import Application as Application
from umlfri2.constants.paths import OS_SPECIFIC_ICON_THEME_PATH as OS_SPECIFIC_ICON_THEME_PATH

NT_ICON_THEME: str

class Win32Specials(OSSpecials):
    def init(self) -> None: ...
