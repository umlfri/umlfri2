import os.path


def get_path(type):
    path = []
    tmp = type
    while tmp.parent is not None:
        path.insert(0, tmp)
        tmp = tmp.parent
    
    if type.type_name == 'Namespace':
        path = [part.identifier.lower_case for part in path] + ['__init__.py']
    else:
        path = [part.identifier.lower_case for part in path[:-1]]\
               + [path[-1].identifier.lower_case + '.py']
    
    return os.path.join(* ['.'] + path)


def name_to_string(type):
    if type.typeName == 'Namespace':
        return type.identifier.lower_camel_case
    else:
        return type.identifier.upper_camel_case


def get_fqn(type):
    path = []
    tmp = type
    while tmp.parent is not None:
        path.insert(0, tmp)
        tmp = tmp.parent
    
    return '.'.join(name_to_string(part) for part in path)


def get_import_path(type, relative_to=None):
    relativity = []
    
    if relative_to is None:
        path = []
        tmp = type
        while tmp.parent is not None:
            path.insert(0, tmp)
            tmp = tmp.parent
    else:
        tmp2 = relative_to
        while tmp2.parent is not None:
            relativity.append('.')
            
            path = []
            tmp = type
            while tmp.parent is not None:
                path.insert(0, tmp)
                
                if tmp.parent is tmp2.parent:
                    break
                
                tmp = tmp.parent
            else:
                tmp2 = tmp2.parent
                continue
            
            break
    
    return ''.join(relativity) + '.'.join(part.identifier.lower_case for part in path)
