def compute_interface_api_name(name):
    return ('I' + name).upper_camel_case


def compute_method_api_name(singular):
    return singular.upper_camel_case


def compute_method_parameter_api_name(singular):
    return singular.lower_camel_case


def compute_property_index_api_name(singular):
    return singular.lower_camel_case


def compute_property_getter_api_name(singular, plural):
    return ('get' + singular).upper_camel_case


def compute_property_setter_api_name(singular, plural):
    return ('set' + singular).upper_camel_case


def compute_property_iterator_api_name(singular, plural):
    return ('get' + plural).upper_camel_case


def compute_event_api_name(identifier):
    return identifier.lower_dash_separated
