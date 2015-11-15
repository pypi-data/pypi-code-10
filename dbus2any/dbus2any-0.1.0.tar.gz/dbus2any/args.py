# -*- coding: utf-8 -*-

meta_args = (
    {
        'name': '--list',
        'flag': '-l',
        'action': 'store_true',
        'help': 'list template names'
    },
    {
        'name': '--template',
        'flag': '-t',
        'metavar': 'template',
        'type': str,
        'help':'template name or url to template'
    },
    {
        'name': '--busName',
        'flag': '-n',
        'metavar': 'busName',
        'type':str,
        'help':'dbus name for object that you want convert'
    },
    {
        'name': '--objectPath',
        'flag': '-p',
        'metavar': 'objectPath',
        'type':str,
        'help':'dbus object path for object that you want convert'
    },
    {
        'name': '--interface',
        'flag': '-i',
        'metavar':'interface',
        'type':str,
        'help':'interface if you want show to especific interface'
    },
    {
        'name': '--xml',
        'flag': '-x',
        'metavar': 'xml',
        'type':str,
        'help': 'xml path of dbus object interfaces'
    }
)

def get_args():
    import argparse
    parser = argparse.ArgumentParser(prog='dbustoany',
        description='Convert dbus interfaces xml in code')
    for v in meta_args:
        flags = [v['name']]
        del v['name']
        if 'flag' in v:
            flags.append(v['flag'])
            del v['flag']
        parser.add_argument(*flags, **v)
    return parser.parse_args()

