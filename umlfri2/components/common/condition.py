from .controlcomponent import ControlComponent


class Condition(ControlComponent):
    def __init__(self, children, condition: bool):
        super().__init__(children)
        self.__condition = condition
    
    def filter_children(self, context):
        if self.__condition(context):
            yield from self._get_children(context)
