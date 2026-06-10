from .box import BoxComponent as BoxComponent, BoxObject as BoxObject
from umlfri2.types.geometry import Point as Point, Size as Size

class VBoxObject(BoxObject): ...

class VBoxComponent(BoxComponent):
    def __init__(self, children, expand) -> None: ...
