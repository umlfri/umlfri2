import jinja2


def fix_nones(thing):
    if thing is None:
        return ''
    else:
        return thing


JINJA_ENV = jinja2.Environment(finalize=fix_nones)
JINJA_ENV.globals['sorted'] = sorted
JINJA_ENV.globals['len'] = len
JINJA_ENV.globals['repr'] = repr