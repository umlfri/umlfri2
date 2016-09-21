class FontStyle:
    @staticmethod
    def to_string(style):
        if style == FontStyle.italic:
            return "italic"
        elif style == FontStyle.bold:
            return "bold"
        elif style == FontStyle.underline:
            return "underline"
        elif style == FontStyle.strike:
            return "strike"
        else:
            raise Exception
    
    italic = 1
    bold = 2
    underline = 3
    strike = 4
