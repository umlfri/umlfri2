from PyQt5.QtGui import QIcon

from umlfri2.constants.paths import OS_SPECIFIC_ICON_THEME_PATH


MAC_OS_ICON_THEME = 'macMint'


def apply():
    QIcon.setThemeSearchPaths([OS_SPECIFIC_ICON_THEME_PATH])
    QIcon.setThemeName(MAC_OS_ICON_THEME)
