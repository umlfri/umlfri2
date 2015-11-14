from .action import Action


class AddConnectionAction(Action):
    def __init__(self, type):
        super().__init__()
        self.__type = type
