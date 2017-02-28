from .pathpartcomponent import PathPartComponent


class Close(PathPartComponent):
    def add_to_path(self, context, builder):
        builder.close()
