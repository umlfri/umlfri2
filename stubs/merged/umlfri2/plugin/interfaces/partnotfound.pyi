from .interfaceexception import InterfaceException as InterfaceException

class PartNotFound(InterfaceException):
    def __init__(self, name) -> None: ...
