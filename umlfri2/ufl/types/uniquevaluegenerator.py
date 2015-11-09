from umlfri2.components.base.context import Context


class UniqueValueGenerator:
    def get_text(self, template):
        i = 1
        prev = None
        context = Context().extend(self.get_parent_name(), 'parent')
        
        while True:
            new = template.get_text(context.extend(i, 'no'))
            if new == prev:
                return "" # cant find template
            
            if not self.has_value(new):
                return new
            
            i += 1
            prev = new
    
    def get_parent_name(self):
        raise NotImplementedError
    
    def has_value(self, value):
        raise NotImplementedError
    
    def for_name(self, name):
        raise NotImplementedError
