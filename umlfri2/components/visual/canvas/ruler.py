import abc


class Ruler(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def measure_text(self, font, text):
        pass
    
    @abc.abstractmethod
    def measure_image(self, image):
        pass
