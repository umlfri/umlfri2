from ....types.generic import UflAnyType, UflAnyWithDefault, UflGenericType
from ....types.structured import UflNullableType
from ...signature import MacroSignature
from ...inlined import InlinedMacro
from ....uniquevaluegenerator import UniqueValueGenerator


class DefaultUniqueValueGenerator(UniqueValueGenerator):
    def get_parent_name(self):
        return 'default'

    def has_value(self, value):
        return False

    def for_name(self, name):
        return self


class DefaultMacro(InlinedMacro):
    src_type = UflGenericType(UflAnyWithDefault())
    
    signature = MacroSignature(
        'default',
        UflNullableType(src_type),
        [],
        src_type
    )
    
    def compile(self, visitor, registrar, node):
        inner_type = node.target.type.inner_type
        
        def default(nullable):
            if nullable is None:
                return inner_type.build_default(DefaultUniqueValueGenerator())
            else:
                return nullable
        
        py_default = registrar.register_function(default)
        
        target = node.target.accept(visitor)
        
        return "{0}({1})".format(py_default, target)


class DefaultWithValueMacro(InlinedMacro):
    src_type = UflGenericType(UflAnyType())
    
    signature = MacroSignature(
        'default',
        UflNullableType(src_type),
        [src_type],
        src_type
    )
    
    def compile(self, visitor, registrar, node):
        py_default = registrar.register_function(self.__default)
        
        target = node.target.accept(visitor)
        
        default_value = node.arguments[0].accept(visitor)
        
        return "{0}(({1}), ({2}))".format(py_default, target, default_value)
    
    @staticmethod
    def __default(nullable, default):
        if nullable is None:
            return default
        else:
            return nullable
