#!/usr/bin/python3

import gettext
import sys

import lxml.etree
from PySide.QtGui import QApplication

from umlfri2.application import Application
from umlfri2.datalayer.loaders.projectloader import ProjectLoader
from umlfri2.model import Solution
from umlfri2.qtgui.base.qtruler import QTRuler
from umlfri2.qtgui import UmlFriMainWindow

app = QApplication(sys.argv)

gettext.install('umlfri2')

Application().use_ruler(QTRuler())

window = UmlFriMainWindow()
window.showMaximized()

sys.exit(app.exec_())
