def compute_interface_api_name(name):
    return name.upper_camel_case


def compute_method_api_name(singular):
    return singular.lower_underscore_separated


def compute_method_parameter_api_name(singular):
    return singular.lower_underscore_separated


def compute_property_index_api_name(singular):
    return singular.lower_underscore_separated


def compute_property_getter_api_name(singular, plural):
    return ('get' + singular).lower_underscore_separated


def compute_property_setter_api_name(singular, plural):
    return ('set' + singular).lower_underscore_separated


def compute_property_iterator_api_name(singular, plural):
    return ('get' + plural).lower_underscore_separated


def compute_event_registrar_api_name(identifier):
    return ('register' + identifier).lower_underscore_separated


def compute_event_deregistrar_api_name(identifier):
    return ('deregister' + identifier).lower_underscore_separated
