from .base import OSSpecials as OSSpecials
from umlfri2.constants.paths import OS_SPECIFIC_ICON_THEME_PATH as OS_SPECIFIC_ICON_THEME_PATH

MAC_OS_ICON_THEME: str

class MacOsXSpecials(OSSpecials):
    def init(self) -> None: ...
