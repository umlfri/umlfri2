#!/usr/bin/python3

import gettext
import os
import sys

import lxml.etree
from PySide.QtGui import QApplication

from umlfri2.application import Application
from umlfri2.datalayer.loaders.projectloader import ProjectLoader
from umlfri2.model import Solution
from umlfri2.qtgui.base.qtruler import QTRuler
from umlfri2.qtgui import UmlFriMainWindow

if os.name == 'nt':
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("FriUniza.UmlFri.{0}".format(Application().VERSION))

app = QApplication(sys.argv)

gettext.install('umlfri2')

Application().use_ruler(QTRuler())

window = UmlFriMainWindow()
window.showMaximized()

sys.exit(app.exec_())
