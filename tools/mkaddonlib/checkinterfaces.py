from lib.checker.writer import UmlFriInterfaceWriter
from lib.model import Builder
from lib.checker import UmlFriInterfaceLoader

builder = Builder()

builder.parse()
builder.finish()

loader = UmlFriInterfaceLoader()
interfaces = loader.load()
interfaces = interfaces.fix_from(builder.get_type_by_type('Interface'))
writer = UmlFriInterfaceWriter(interfaces)
writer.write_to('checked_api')
