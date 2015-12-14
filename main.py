#!/usr/bin/python3

import gettext
import os
import sys

from PySide.QtGui import QApplication, QIcon

from umlfri2.application import Application
from umlfri2.constants.paths import NT_ICON_THEME_PATH, NT_ICON_THEME, LOCALE_DIR
from umlfri2.qtgui import UmlFriMainWindow
from umlfri2.qtgui.base.qtruler import QTRuler

if os.name == 'nt':
    import ctypes
    SetCurrentProcessExplicitAppUserModelID = getattr(ctypes.windll.shell32, 'SetCurrentProcessExplicitAppUserModelID', None)
    
    if SetCurrentProcessExplicitAppUserModelID is not None:
        SetCurrentProcessExplicitAppUserModelID("FriUniza.UmlFri.{0}".format(Application().VERSION))

    QIcon.setThemeSearchPaths([NT_ICON_THEME_PATH])
    QIcon.setThemeName(NT_ICON_THEME)

app = QApplication(sys.argv)

gettext.translation('umlfri2', localedir=LOCALE_DIR, languages=[Application().language], fallback=True).install()

Application().use_ruler(QTRuler())

window = UmlFriMainWindow()
window.showMaximized()

sys.exit(app.exec_())
