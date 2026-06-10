from _typeshed import Incomplete

class Component:
    ATTRIBUTES: Incomplete
    CHILDREN_ATTRIBUTES: Incomplete
    HAS_CHILDREN: bool
    CHILDREN_TYPE: Incomplete
    IS_CONTROL: bool
    IS_HELPER: bool
    SPECIAL_CHILDREN: Incomplete
    ONLY_SPECIAL_CHILDREN: bool
    def __init__(self, children) -> None: ...
    def compile(self, type_context) -> None: ...
