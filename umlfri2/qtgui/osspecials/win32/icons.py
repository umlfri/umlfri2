from PyQt5.QtGui import QIcon

from umlfri2.constants.paths import NT_ICON_THEME_PATH, NT_ICON_THEME


def apply():
    QIcon.setThemeSearchPaths([NT_ICON_THEME_PATH])
    QIcon.setThemeName(NT_ICON_THEME)
