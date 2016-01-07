class Documentation(str):
    def indent(self, indentation, indent_first_line=False, char=' '):
        indent = char * indentation
        ret = ('\n' + indent).join(self.split('\n'))
        
        if indent_first_line:
            ret = indent + ret
        
        return Documentation(ret)
    
    @property
    def first_sentence(self):
        if '.' in self:
            sentences = self.split('.')
            ret = sentences.pop(0) + '.'
            while len(sentences) > 0 and sentences[0].startswith('FRI'):
                ret += sentences.pop(0) + '.'
            return ret
        else:
            return str(self)
