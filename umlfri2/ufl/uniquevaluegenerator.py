from umlfri2.components.base.context import Context


class UniqueValueGenerator:
    def get_text(self, template):
        i = 1
        prev = None
        context = Context().set_variable('parent', self.get_parent_name())
        
        while True:
            new = template.get_text(context.set_variable('no', i))
            if new == prev:
                return new # cant find template
            
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
