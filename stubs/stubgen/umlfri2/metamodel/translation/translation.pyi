from ..connectiontype import ConnectionType as ConnectionType
from ..diagramtype import DiagramType as DiagramType
from ..elementtype import ElementType as ElementType
from ..projecttemplate import ProjectTemplate as ProjectTemplate
from .attributetranslation import AttributeTranslation as AttributeTranslation
from .configattributetransslation import ConfigAttributeTranslation as ConfigAttributeTranslation
from _typeshed import Incomplete
from umlfri2.ufl.types.enum import UflEnumPossibility as UflEnumPossibility
from umlfri2.ufl.types.structured import UflObjectAttribute as UflObjectAttribute

class Translation:
    def __init__(self, language, translations) -> None: ...
    @property
    def language(self): ...
    def translate(self, object): ...

POSIX_TRANSLATION: Incomplete
