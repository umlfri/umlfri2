from .file import File
from .generator import Generator
from .template import Template
from .directory import Directory
from .jinjaenv import JINJA_ENV

import sys
import os.path
import lxml.etree


class FileList:
    def __init__(self, builder):
        self.__fileList = []
        self.__builder = builder
        self.__modules = {}
    
    def parse(self, path):
        dir = os.path.dirname(path)
        rel = lambda f: os.path.abspath(os.path.join(dir, f))
        
        lib_dir = os.path.join(dir, 'lib')
        if os.path.exists(lib_dir):
            sys.path.append(lib_dir)
            for name in os.listdir(lib_dir):
                if name.endswith('.py'):
                    name = name[:-3]
                    self.__modules[name] = __import__(name)
        
        if path.endswith('.py'):
            locals = {}
            globals = {}
            with open(path) as py_file:
                exec(py_file.read(), globals, locals)
            for type, params in locals['generate'](self.__builder.get_root_namespace()):
                if type == 'file':
                    self.__append_file(rel(params[0]), params[1])
                elif type == 'generator':
                    self.__append_generator(rel(params[0]), params[1], params[2])
                elif type == 'template':
                    self.__append_template(rel(params[0]), params[1], params[2])
        else:
            if path.endswith('.xml'):
                data = lxml.etree.parse(path).getroot()
            elif path.endswith('.xml.tmpl'):
                with open(path) as template_file:
                    data = lxml.etree.XML(
                        JINJA_ENV.from_string(template_file.read()).render(root=self.__builder.get_root_namespace(),
                                                                   **self.__modules)
                    )
            else:
                raise Exception
            
            for child in data.getchildren():
                if child.tag == 'file':
                    self.__append_file(rel(child.attrib['path']), child.attrib['output'])
                elif child.tag == 'generator':
                    self.__append_generator(rel(child.attrib['path']), child.attrib['output'], child.attrib['root'] or None)
                elif child.tag == 'template':
                    self.__append_template(rel(child.attrib['path']), child.attrib['output'], child.attrib['root'] or None)
                elif child.tag == 'directory':
                    self.__append_directory(rel(child.attrib['path']), child.attrib['output'], child.attrib['glob'])
    
    def create(self, dir):
        for f in self.__fileList:
            f.create(dir)
    
    def __append_file(self, inputFile, outputFile):
        self.__fileList.append(File(inputFile, outputFile))
    
    def __append_generator(self, inputFile, outputFile, fqn):
        self.__fileList.append(Generator(inputFile, outputFile, self.__builder.get_type_by_fqn(fqn)))
            
    def __append_template(self, inputFile, outputFile, fqn):
        self.__fileList.append(Template(inputFile, outputFile, self.__builder.get_type_by_fqn(fqn), self.__modules))
            
    def __append_directory(self, inputFile, outputFile, glob):
        self.__fileList.append(Directory(inputFile, outputFile, glob))
