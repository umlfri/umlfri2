from optparse import OptionParser

import sys

from lib.checker.writer import UmlFriInterfaceWriter
from lib.model import Builder
from lib.checker import UmlFriInterfaceLoader


def main(*args):
    options_parser = OptionParser(usage = "usage: %prog [options]")
    options_parser.add_option("-o", "--output", dest="output_directory", default="output/",
                      help="write output to DIR", metavar="DIR")
    
    (options, args) = options_parser.parse_args(list(args))
    
    builder = Builder()
    
    builder.parse()
    builder.finish()
    
    loader = UmlFriInterfaceLoader()
    
    interfaces = loader.load()
    interfaces = interfaces.fix_from(builder.get_type_by_type('Interface'))
    
    writer = UmlFriInterfaceWriter(interfaces)
    writer.write_to(options.output_directory)

main(*sys.argv[1:])
