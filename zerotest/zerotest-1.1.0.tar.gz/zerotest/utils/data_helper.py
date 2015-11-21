def delete_path_from_dict(d, path):
    """
    delete key path from dict
    :param d: dict
    :param path: key path example: a.b.c
    :return:
    """
    if not d:
        return
    paths = path.split('.')
    parent = d
    last_path = ''
    for i, p in enumerate(paths):
        if not d:
            return
        elif isinstance(d, list):
            for item in d:
                delete_path_from_dict(item, '.'.join(paths[i:]))
            return

        last_path = p
        parent = d
        d = d.get(p)

    parent.pop(last_path, None)
