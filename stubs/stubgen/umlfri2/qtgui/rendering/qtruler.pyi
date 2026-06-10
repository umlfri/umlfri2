from umlfri2.qtgui.base import image_loader as image_loader
from umlfri2.types.font import FontStyle as FontStyle
from umlfri2.types.geometry import Size as Size
from umlfri2.ufl.components.visual.canvas import Ruler as Ruler

class QTRuler(Ruler):
    def measure_text(self, font, text): ...
    def measure_image(self, image): ...
