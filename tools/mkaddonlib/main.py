#!/usr/bin/env python3

import sys

from lib.model import Builder
from lib.generator import FileList
from optparse import OptionParser


def main(*args):
    options_parser = OptionParser(usage = "usage: %prog [options] index1 [index2 [...]]")
    options_parser.add_option("-o", "--output", dest="output_directory", default="output/",
                      help="write output to DIR", metavar="DIR")
    
    (options, args) = options_parser.parse_args(list(args))
    
    if not args:
        options_parser.print_help()
        sys.exit()
    
    builder = Builder()
    
    builder.parse()
    builder.finish()
    
    #builder.validate()
    
    out = FileList(builder)
    
    for index in args:
        out.parse(index)
    
    out.create(options.output_directory)

main(*sys.argv[1:])
