from PyQt5.QtGui import QIcon

from umlfri2.constants.paths import OS_SPECIFIC_ICON_THEME_PATH

from .base import OSSpecials


MAC_OS_ICON_THEME = 'macMint'


class MacOsXSpecials(OSSpecials):
    def __apply_icons(self):
        QIcon.setThemeSearchPaths([OS_SPECIFIC_ICON_THEME_PATH])
        QIcon.setThemeName(MAC_OS_ICON_THEME)
    
    def init(self):
        self.__apply_icons()
