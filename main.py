#!/usr/bin/env python3

import sys

from PyQt5.QtWidgets import QApplication

from umlfri2.application import Application
from umlfri2.qtgui import SplashScreen
from umlfri2.qtgui.base.qtthreadmanager import QTThreadManager
from umlfri2.qtgui.exceptionhook import install_exception_hook
from umlfri2.qtgui.rendering import QTRuler
from umlfri2.qtgui.osspecials import apply_os_specials

def main(args):
    apply_os_specials()
    
    app = QApplication(args)
    
    Application().use_thread_manager(QTThreadManager())
    Application().use_ruler(QTRuler())
    
    Application().start()
    
    install_exception_hook()
    
    splash = SplashScreen()
    
    splash.start()
    
    no = app.exec_()
    
    Application().stop()
    
    return no


if __name__ == "__main__":
    sys.exit(main(sys.argv))
