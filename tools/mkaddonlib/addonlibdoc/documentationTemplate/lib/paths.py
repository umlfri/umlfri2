def get_path(type):
    path = []
    tmp = type
    while tmp.parent is not None:
        path.insert(0, tmp)
        tmp = tmp.parent
    
    path = [part.identifier.lower_camel_case for part in path]
    
    return '.'.join(path) + '.html'
