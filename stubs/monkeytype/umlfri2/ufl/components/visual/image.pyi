from umlfri2.ufl.components.valueproviders.dynamic import DynamicValueProvider
from umlfri2.ufl.context.typecontext import TypeContext


class ImageComponent:
    def __init__(self, image: DynamicValueProvider) -> None: ...
    def compile(self, type_context: TypeContext) -> None: ...
