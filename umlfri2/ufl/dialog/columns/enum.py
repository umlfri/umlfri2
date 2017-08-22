from .column import UflDialogColumn


class UflDialogEnumColumn(UflDialogColumn):
    def __init__(self, attr):
        super().__init__(attr)
        
        self.__possibilities = tuple(attr.type.possibilities)
        self.__values = {}

    def get_value(self, object):
        value = self._get_real_value(object)
        
        return self.__values.get(value, value)
    
    def translate(self, translation):
        super().translate(translation)

        self.__values = {x.value: translation.translate(x) for x in self.__possibilities}
