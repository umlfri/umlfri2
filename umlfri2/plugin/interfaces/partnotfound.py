from .interfaceexception import InterfaceException


class PartNotFound(InterfaceException):
    def __init__(self, name):
        super().__init__({'name': name})
