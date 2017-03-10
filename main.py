#!/usr/bin/env python3

import sys

from PyQt5.QtWidgets import QApplication

from umlfri2.application import Application
from umlfri2.qtgui import SplashScreen
from umlfri2.qtgui.base.gtkstylefix import set_gtk_icon_theme_if_needed
from umlfri2.qtgui.base.qtthreadmanager import QTThreadManager
from umlfri2.qtgui.rendering import QTRuler
from umlfri2.qtgui.osspecials import apply_os_specials

def main(args):
    apply_os_specials()
    
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
