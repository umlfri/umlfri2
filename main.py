#!/usr/bin/env python3

import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from umlfri2.application import Application
from umlfri2.constants.paths import NT_ICON_THEME_PATH, NT_ICON_THEME
from umlfri2.qtgui import SplashScreen
from umlfri2.qtgui.base.gtkstylefix import set_gtk_icon_theme_if_needed
from umlfri2.qtgui.base.qtthreadmanager import QTThreadManager
from umlfri2.qtgui.rendering import QTRuler


def main(args):
    if os.name == 'nt':
        import ctypes
        SetCurrentProcessExplicitAppUserModelID = getattr(ctypes.windll.shell32, 'SetCurrentProcessExplicitAppUserModelID', None)
        
        if SetCurrentProcessExplicitAppUserModelID is not None:
            SetCurrentProcessExplicitAppUserModelID("FriUniza.UmlFri.{0}".format(Application().VERSION))
    
        QIcon.setThemeSearchPaths([NT_ICON_THEME_PATH])
        QIcon.setThemeName(NT_ICON_THEME)
    
    app = QApplication(args)
    
    set_gtk_icon_theme_if_needed()
    
    Application().use_thread_manager(QTThreadManager())
    Application().use_ruler(QTRuler())
    
    Application().start()

    splash = SplashScreen()
    
    splash.start()
    
    no = app.exec_()
    
    Application().stop()
    
    return no


if __name__ == "__main__":
    sys.exit(main(sys.argv))
