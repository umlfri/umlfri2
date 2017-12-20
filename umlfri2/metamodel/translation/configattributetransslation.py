from .attributetranslation import AttributeTranslation


class ConfigAttributeTranslation(AttributeTranslation):
    def translate(self, object):
        from ..metamodel import Metamodel
        if isinstance(object, Metamodel) and not self.has_parents:
            return self.label
        return super().translate(object)
