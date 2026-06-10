from .pathpartcomponent import PathPartComponent as PathPartComponent

class Close(PathPartComponent):
    def add_to_path(self, context, builder) -> None: ...
