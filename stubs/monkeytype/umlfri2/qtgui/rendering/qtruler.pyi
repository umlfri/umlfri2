from umlfri2.types.font import Font
from umlfri2.types.geometry.size import Size


class QTRuler:
    def measure_text(self, font: Font, text: str) -> Size: ...
