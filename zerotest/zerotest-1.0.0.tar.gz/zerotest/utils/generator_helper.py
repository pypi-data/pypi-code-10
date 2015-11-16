__author__ = 'Hari Jiang'


def get_name_from_request(request):
    return '{}_{}'.format(request.method.lower(), _path_to_func_name(request.path))


def _path_to_func_name(path):
    if path == '/':
        name = 'root'
    else:
        name = path[1:].replace('/', '_').replace('-', '_')
    return name


def dict_to_param_style_code(d):
    source = ", ".join(map(lambda (k, v): "{}={}".format(k, repr(v)), d.items()))
    return source
