from .basecontainer import BaseContainer
from .delegate import Delegate
from .delegateparameter import DelegateParameter
from .delegatereturn import DelegateReturn
from .delegatethrows import DelegateThrows
from .documentation import Documentation
from .exception import Exception as ExceptionDefinition
from .exceptionproperty import ExceptionProperty
from .interface import Interface
from .interfaceevent import InterfaceEvent
from .interfaceeventregistrar import InterfaceEventRegistrar
from .interfaceeventderegistrar import InterfaceEventDeregistrar
from .interfacemethod import InterfaceMethod
from .interfacemethodparameter import InterfaceMethodParameter
from .interfacemethodreturn import InterfaceMethodReturn
from .interfacemethodthrows import InterfaceMethodThrows
from .interfaceproperty import InterfaceProperty
from .interfacepropertygetter import InterfacePropertyGetter
from .interfacepropertyindex import InterfacePropertyIndex
from .interfacepropertyiterator import InterfacePropertyIterator
from .interfacepropertysetter import InterfacePropertySetter
from .interfacepropertythrows import InterfacePropertyThrows
from .namespace import Namespace

import os
import os.path

import lxml.etree


class Builder:
    __xml_schema = lxml.etree.XMLSchema(
        lxml.etree.parse(
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "data", "schema", "api", "api.xsd")
        )
    )

    __xml_definitions = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "data", "api")
    
    __xml_ns = "{{http://umlfri.org/v2/api.xsd}}{0}"
    
    def __init__(self):
        self.__root_namespace = Namespace(None, None)
        self.__cache = {}
    
    def parse(self, dir = None):
        if dir is None:
            dir = self.__xml_definitions
        
        for f in os.listdir(dir):
            if not f.endswith('.xml'):
                continue
            
            root = lxml.etree.parse(os.path.join(dir, f)).getroot()
            if not self.__xml_schema.validate(root):
                raise SyntaxError(self.__xml_schema.error_log.last_error)
            
            if root.tag == self.__xml_ns.format('interface'):
                self.__parse_interface(root)
            elif root.tag == self.__xml_ns.format('exception'):
                self.__parse_exception(root)
            elif root.tag == self.__xml_ns.format('delegate'):
                self.__parse_delegate(root)
    
    def finish(self):
        self.__root_namespace._link(self)
        self.__add_auto_throws()
        self.__add_to_cache(self.__root_namespace)

    def validate(self):
        self.__root_namespace.validate()
    
    def get_root_namespace(self):
        return self.__root_namespace
    
    def print_structure(self):
        def recursion(self, object, level):
            print ('    ' * level) + repr(object), ('with api name ' + repr(object.api_name)) if hasattr(object, 'apiName') else ''
            
            if isinstance(object, BaseContainer):
                for child in object.children:
                    recursion(child, level + 1)
        
        for child in self.__root_namespace.children:
            recursion(child, 0)
    
    def get_type_by_name(self, name):
        namespace, name = self.__parse_namespace_and_name(name)
        type = namespace.get_child(name)
        
        if not isinstance(type, (Interface, Delegate, ExceptionDefinition)):
            raise Exception
        
        return type
    
    def get_type_by_fqn(self, fqn):
        return self.__cache[fqn]
    
    def get_type_by_type(self, *types):
        def recursion(obj):
            if obj.type_name in types:
                yield obj
            elif isinstance(obj, BaseContainer):
                for child in obj.children:
                    yield from recursion(child)
        return recursion(self.__root_namespace)
    
    ################
    ### Interface
    
    def __parse_interface(self, root):
        namespace, name = self.__parse_namespace_and_name(root.attrib['name'])
        try:
            namespace.get_child(name)
        except KeyError:
            pass
        else:
            raise Exception
        
        interface = Interface(
            name,
            namespace,
            api_name=root.attrib.get('apiName'),
            base=root.attrib.get('base'),
            abstract=root.attrib.get('abstract', "false").lower() in ("1", "true"),
            generate=root.attrib.get('generate', "true").lower() in ("1", "true"),
            documentation=self.__parse_documentation(root.find(self.__xml_ns.format('documentation')))
        )
        
        namespace.add_child(interface)
        
        for child in root:
            if child.tag == self.__xml_ns.format('property'):
                self.__parse_interface_property(child, interface)
            elif child.tag == self.__xml_ns.format('method'):
                self.__parse_interface_method(child, interface)
            elif child.tag == self.__xml_ns.format('event'):
                self.__parse_interface_event(child, interface)
    
    def __parse_interface_method(self, root, interface):
        method = InterfaceMethod(
            root.attrib['name'],
            interface,
            api_name=root.attrib.get('apiname'),
            mutator=root.attrib.get('mutator', "false").lower() in ("1", "true"),
            transactional=root.attrib.get('transactional', "true").lower() in ("1", "true"),
            async=root.attrib.get('async', "false").lower() in ("1", "true"),
            documentation=self.__parse_documentation(root.find(self.__xml_ns.format('documentation')))
        )
        
        interface.add_child(method)
        
        for child in root:
            if child.tag == self.__xml_ns.format('parameter'):
                if child.attrib['type'] == 'namedparams':
                    raise Exception
                
                parameter = InterfaceMethodParameter(
                    child.attrib['name'],
                    method,
                    child.attrib['type'],
                    api_name=child.attrib.get('apiname'),
                    required=child.attrib.get('required', "true").lower() in ("1", "true"),
                    nullable=child.attrib.get('nullable', "false").lower() in ("1", "true"),
                    default= child.attrib.get('default'),
                    documentation=self.__parse_documentation(child.find(self.__xml_ns.format('documentation'))),
                )
                method.add_child(parameter)
            elif child.tag == self.__xml_ns.format('parameterDictionary'):
                parameter = InterfaceMethodParameter(
                    child.attrib['name'],
                    method,
                    '*',
                    api_name=child.attrib.get('apiname'),
                    required=True,
                    documentation=self.__parse_documentation(child.find(self.__xml_ns.format('documentation'))),
                )
                method.add_child(parameter)
            elif child.tag == self.__xml_ns.format('return'):
                return_type = InterfaceMethodReturn(
                    method,
                    child.attrib['type'],
                    nullable=child.attrib.get('nullable', "false").lower() in ("1", "true"),
                    iterable=child.attrib.get('iterable', "false").lower() in ("1", "true"),
                    documentation=self.__parse_documentation(child.find(self.__xml_ns.format('documentation'))),
                )
                method.add_child(return_type)
            elif child.tag == self.__xml_ns.format('throws'):
                throws = InterfaceMethodThrows(
                    method,
                    child.attrib['exception'],
                    documentation = self.__parse_documentation(child.find(self.__xml_ns.format('documentation'))),
                )
                method.add_child(throws)
    
    def __parse_interface_property(self, root, interface):
        value = root.find(self.__xml_ns.format('value'))
        index = root.find(self.__xml_ns.format('index'))
        getter = root.find(self.__xml_ns.format('getter'))
        setter = root.find(self.__xml_ns.format('setter'))
        iterator = root.find(self.__xml_ns.format('iterator'))
        
        property = InterfaceProperty(
            root.attrib['name'],
            interface,
            singular=root.attrib.get('singular'),
            nullable=value.attrib.get('nullable', "false").lower() in ("1", "true"),
            type=value.attrib['type'],
            documentation=self.__parse_documentation(root.find(self.__xml_ns.format('documentation')))
        )
        
        interface.add_child(property)
        
        if index is not None:
            property_index = InterfacePropertyIndex(
                index.attrib['name'],
                property,
                type=index.attrib['type'],
                api_name=index.attrib.get('apiname'),
                documentation=self.__parse_documentation(index.find(self.__xml_ns.format('documentation')))
            )
            property.add_child(property_index)
        able_children = 0
        
        if value.attrib.get('readable', "false").lower() in ("1", "true"):
            api_name = None
            
            if getter is not None:
                api_name = getter.attrib.get('apiname')
            
            accessor = InterfacePropertyGetter(
                property,
                api_name=api_name
            )
            property.add_child(accessor)
            
            if getter is not None:
                self.__parse_interface_property_throws(accessor, getter)
            
            able_children += 1
        
        if value.attrib.get('writable', "false").lower() in ("1", "true"):
            api_name = None
            transactional = True
            
            if setter is not None:
                api_name = setter.attrib.get('apiname')
                transactional = setter.attrib.get('transactional', "true").lower() in ("1", "true")
            
            accessor = InterfacePropertySetter(
                property,
                api_name=api_name,
                transactional=transactional
            )
            property.add_child(accessor)
            
            if setter is not None:
                self.__parse_interface_property_throws(accessor, setter)
            
            able_children += 1
        
        if value.attrib.get('iterable', "false").lower() in ("1", "true"):
            api_name = None
            
            if iterator is not None:
                api_name = iterator.attrib.get('apiname')
            
            accessor = InterfacePropertyIterator(
                property,
                api_name=api_name
            )
            property.add_child(accessor)
            
            if iterator is not None:
                self.__parse_interface_property_throws(accessor, iterator)
            
            able_children += 1
        
        if able_children == 0:
            raise Exception()
    
    def __parse_interface_property_throws(self, method, root):
        for child in root:
            if child.tag == self.__xml_ns.format('throws'):
                throws = InterfacePropertyThrows(
                    method,
                    child.attrib['exception'],
                    documentation=self.__parse_documentation(child.find(self.__xml_ns.format('documentation'))),
                )
                method.add_child(throws)
    
    def __parse_interface_event(self, root, interface):
        registrar = root.find(self.__xml_ns.format('registrar'))
        deregistrar = root.find(self.__xml_ns.format('deregistrar'))
        
        event = InterfaceEvent(
            root.attrib['name'],
            interface,
            type=root.attrib['type'],
            documentation=self.__parse_documentation(root.find(self.__xml_ns.format('documentation')))
        )
        
        if registrar is not None:
            registrar_api_name = registrar.attrib.get('apiname')
        else:
            registrar_api_name = None
        
        if deregistrar is not None:
            deregistrar_api_name = deregistrar.attrib.get('apiname')
        else:
            deregistrar_api_name = None
        
        event.add_child(InterfaceEventRegistrar(event, registrar_api_name))
        event.add_child(InterfaceEventDeregistrar(event, deregistrar_api_name))
        
        interface.add_child(event)
    
    ################
    ### Exception
    
    def __parse_exception(self, root):
        namespace, name = self.__parse_namespace_and_name(root.attrib['name'])
        try:
            namespace.get_child(name)
        except KeyError:
            pass
        else:
            raise Exception
        
        exception = ExceptionDefinition(
            name,
            namespace,
            number=int(root.attrib['number']),
            base=root.attrib.get('base'),
            throws_from=root.attrib.get('throwsFrom'),
            documentation=self.__parse_documentation(root.find(self.__xml_ns.format('documentation')))
        )
        namespace.add_child(exception)
        
        for child in root:
            if child.tag == self.__xml_ns.format('property'):
                value = child.find(self.__xml_ns.format('value'))
                
                iterable = value.attrib.get('iterable', 'false').lower() in ('1', 'true')
                readable = value.attrib.get('readable', 'false').lower() in ('1', 'true')
                
                if not (iterable or readable) or (iterable and readable):
                    raise Exception()
                
                property = ExceptionProperty(
                    child.attrib['name'],
                    exception,
                    type=value.attrib['type'],
                    index=int(child.attrib['index']),
                    iterable=iterable,
                    documentation=self.__parse_documentation(child.find(self.__xml_ns.format('documentation')))
                )
                exception.add_child(property)
    
    ################
    ### Delegate
    
    def __parse_delegate(self, root):
        namespace, name = self.__parse_namespace_and_name(root.attrib['name'])
        try:
            namespace.get_child(name)
        except KeyError:
            pass
        else:
            raise Exception
        
        delegate = Delegate(
            name,
            namespace,
            documentation = self.__parse_documentation(root.find(self.__xml_ns.format('documentation')))
        )
        namespace.add_child(delegate)
        
        for child in root:
            if child.tag == self.__xml_ns.format('parameter'):
                if child.attrib['type'] == 'namedparams':
                    raise Exception
                
                parameter = DelegateParameter(
                    child.attrib['name'],
                    delegate,
                    child.attrib['type'],
                    api_name=child.attrib.get('apiname'),
                    required=child.attrib.get('required', "true").lower() in ("1", "true"),
                    default=child.attrib.get('default'),
                    documentation=self.__parse_documentation(child.find(self.__xml_ns.format('documentation'))),
                )
                delegate.add_child(parameter)
            elif child.tag == self.__xml_ns.format('parameterDictionary'):
                parameter = DelegateParameter(
                    child.attrib['name'],
                    delegate,
                    '*',
                    api_name=child.attrib.get('apiname'),
                    required=True,
                    documentation=self.__parse_documentation(child.find(self.__xml_ns.format('documentation'))),
                )
                delegate.add_child(parameter)
            elif child.tag == self.__xml_ns.format('return'):
                return_type = DelegateReturn(
                    delegate,
                    child.attrib['type'],
                    iterable=child.attrib.get('iterable', "true").lower() in ("1", "true"),
                    documentation=self.__parse_documentation(child.find(self.__xml_ns.format('documentation'))),
                )
                delegate.add_child(return_type)
            elif child.tag == self.__xml_ns.format('throws'):
                throws = DelegateThrows(
                    delegate,
                    child.attrib['exception'],
                    documentation=self.__parse_documentation(child.find(self.__xml_ns.format('documentation'))),
                )
                delegate.add_child(throws)
    
    ################
    ### Helpers
    
    def __parse_namespace_and_name(self, fqn):
        symbols = fqn.split('.')
        
        name = symbols.pop()
        
        namespace = self.__root_namespace
        
        for symbol in symbols:
            try:
                namespace = namespace.get_child(symbol)
                if not isinstance(namespace, Namespace):
                    raise Exception()
            except KeyError:
                parent = namespace
                namespace = Namespace(symbol, parent)
                parent.add_child(namespace)
        
        return namespace, name
    
    def __parse_documentation(self, documentation):
        if documentation is None:
            return None
        
        text = documentation.text
        
        return Documentation('\n'.join(line.strip() for line in text.strip().split('\n')))
    
    def __add_to_cache(self, object):
        if object.fqn in self.__cache:
            raise Exception("{0} is already in cache".format(object.fqn))
        
        self.__cache[object.fqn] = object
        
        if isinstance(object, BaseContainer):
            for child in object.children:
                self.__add_to_cache(child)

    ########################
    # Auto throws processing
    
    def __add_auto_throws(self):
        exceptions = {'all': [], 'mutator': [], 'transactional': [], 'getter': [], 'setter': [], 'iterator': []}
        self.__find_auto_throws(self.__root_namespace, exceptions)
        self.__set_auto_throws(self.__root_namespace, exceptions)
    
    def __find_auto_throws(self, ns, exceptions):
        for child in ns.children:
            if isinstance(child, Namespace):
                self.__find_auto_throws(child, exceptions)
            elif isinstance(child, ExceptionDefinition):
                for type in child.throws_from:
                    exceptions[type].append(child)
    
    def __set_auto_throws(self, ns, exceptions):
        for child in ns.children:
            if isinstance(child, Namespace):
                self.__set_auto_throws(child, exceptions)
            elif isinstance(child, Interface):
                for member in child.children:
                    if isinstance(member, InterfaceMethod):
                        self.__set_auto_throws_to_method(member, exceptions['all'])
                        if member.mutator:
                            self.__set_auto_throws_to_method(member, exceptions['mutator'])
                        if member.transactional:
                            self.__set_auto_throws_to_method(member, exceptions['transactional'])
                    elif isinstance(member, InterfaceProperty):
                        if member.getter is not None:
                            self.__set_auto_throws_to_property(member.getter, exceptions['all'])
                            self.__set_auto_throws_to_property(member.getter, exceptions['getter'])
                        if member.setter is not None:
                            self.__set_auto_throws_to_property(member.setter, exceptions['all'])
                            self.__set_auto_throws_to_property(member.setter, exceptions['setter'])
                            self.__set_auto_throws_to_property(member.setter, exceptions['mutator'])
                            if member.setter.transactional:
                                self.__set_auto_throws_to_property(member.setter, exceptions['transactional'])
                        if member.iterator is not None:
                            self.__set_auto_throws_to_property(member.iterator, exceptions['all'])
                            self.__set_auto_throws_to_property(member.iterator, exceptions['iterator'])
    
    def __set_auto_throws_to_method(self, member, exceptions):
        for exc in exceptions:
            throws = InterfaceMethodThrows(member, exc)
            member.add_child(throws)
    
    def __set_auto_throws_to_property(self, member, exceptions):
        for exc in exceptions:
            throws = InterfacePropertyThrows(member, exc)
            member.add_child(throws)
