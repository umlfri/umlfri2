from PyQt5.QtGui import QIcon

from umlfri2.constants.paths import OS_SPECIFIC_ICON_THEME_PATH


NT_ICON_THEME = 'oxygen'


def apply():
    QIcon.setThemeSearchPaths([OS_SPECIFIC_ICON_THEME_PATH])
    QIcon.setThemeName(NT_ICON_THEME)
