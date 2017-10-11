import ctypes

from umlfri2.application import Application


def apply():
    SetCurrentProcessExplicitAppUserModelID = getattr(ctypes.windll.shell32, 'SetCurrentProcessExplicitAppUserModelID',
                                                      None)

    if SetCurrentProcessExplicitAppUserModelID is not None:
        SetCurrentProcessExplicitAppUserModelID("FriUniza.UmlFri.{0}".format(Application().about.version.major_minor_string))
