from umlfri2.types.enums import FontStyle


class Font:
    def __init__(self, family, size, style=()):
        self.__family = family
        self.__size = size
        self.__style = frozenset(style)
    
    @property
    def size(self):
        return self.__size
    
    @property
    def family(self):
        return self.__family
    
    @property
    def style(self):
        return self.__style
    
    def change(self, style, value):
        new_style = set(self.__style)
        
        if value:
            new_style.add(style)
        elif style in new_style:
            new_style.remove(style)
        return Font(self.__family, self.__size, new_style)
    
    def __str__(self):
        if self.__style:
            return "{0} {1} {2}".format(self.__family, ' '.join(str(i) for i in self.__style), self.__size)
        else:
            return "{0} {1}".format(self.__family, self.__size)
    
    @staticmethod
    def get_font(description):
        tmp = description.split()
        size = int(tmp.pop(-1))
        
        style = set()
        while tmp[-1] in ('bold', 'italic', 'underline', 'strike'):
            style.add(getattr(FontStyle, tmp.pop(-1)))
        
        family = ' '.join(tmp)
        
        return Font(family, size, style)
