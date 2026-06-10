from ..base import image_loader as image_loader
from PyQt5.QtWidgets import QMenu
from umlfri2.types.geometry import Point as Point

class ActionMenu(QMenu):
    def __init__(self, drawing_area, menu) -> None: ...
    def do(self) -> None: ...
