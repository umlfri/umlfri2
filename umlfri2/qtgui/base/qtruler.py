from PySide.QtGui import QFont, QFontMetrics
from umlfri2.components.visual.canvas import Ruler
from umlfri2.types.font import FontStyle
from umlfri2.types.geometry import Size


class QTRuler(Ruler):
    def measure_text(self, font, text):
        qfont = QFont(font.family)
        qfont.setPixelSize(font.size)
        qfont.setBold(FontStyle.bold in font.style)
        qfont.setItalic(FontStyle.italic in font.style)
        qfont.setStrikeOut(FontStyle.strike in font.style)
        qfont.setUnderline(FontStyle.underline in font.style)
        
        metrics = QFontMetrics(qfont)
        size = metrics.size(0, text)
        return Size(size.width(), size.height())
    
    def measure_image(self, image):
        pass
