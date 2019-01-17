from ....types.generic import UflAnyType, UflGenericType
from ....types.structured import UflIterableType
from ....types.executable import UflLambdaType
from ...signature import MacroSignature
from ...inlined import InlinedMacro


class MapMacro(InlinedMacro):
    src_type = UflGenericType(UflAnyType())
    dest_type = UflGenericType(UflAnyType())
    
    signature = MacroSignature(
        'map',
        UflIterableType(src_type),
        [UflLambdaType([src_type], dest_type)],
        UflIterableType(dest_type)
    )
    
    def compile(self, visitor, registrar, node):
        py_map = registrar.register_function(map)
        
        target = node.target.accept(visitor)
        map_function = node.arguments[0].accept(visitor)
        
        return "{0}(({1}), ({2}))".format(py_map, map_function, target)
