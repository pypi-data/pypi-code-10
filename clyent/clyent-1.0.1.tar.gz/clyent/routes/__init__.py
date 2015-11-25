from __future__ import absolute_import, print_function, unicode_literals

from argparse import ArgumentParser
import inspect


class subcommand:
    def __init__(self, subparsers):
        self.subparsers = subparsers
        self.parser = None
        self.func = None

    def __call__(self, func):

        descr = func.__doc__ or ''
        parser_help = descr.strip().splitlines()[0]
        self.parser = self.subparsers.add_parser('echo', help=parser_help, description=descr)
        self.func = func
        self.parser.set_defaults(subcommand=self)

        if hasattr(self.func, '__cli_args__'):
            for p_args, p_kwargs in self.func.__cli_args__:
                self.parser.add_argument(*p_args, **p_kwargs)

        self.arg_names = add_arguments_from_func(self.func, self.parser)

        return self


def add_arguments_from_func(func, parser):

    spec = inspect.getargspec(func)
    defaults = dict(zip(spec.args[::-1], spec.defaults[::-1]))
    required_args = set(spec.args[:len(spec.args) - len(spec.defaults)])
    actions = {a.dest:a for a in parser._actions}

    for arg_name, default in defaults.items():

        if arg_name not in actions:
            print("adding argument '--%s' to command %s " % (arg_name, func.__name__))
            parser.add_argument('--%s' % arg_name)
            actions = {a.dest:a for a in parser._actions}
        actions[arg_name].default = default

    for arg_name in required_args:
        if arg_name in ['subcommand', 'ctx']:
            continue
        if arg_name not in actions:
            print("adding argument '%s' to command %s " % (arg_name, func.__name__))
            parser.add_argument('%s' % arg_name)
            actions = {a.dest:a for a in parser._actions}

    return spec.args



class command:
    def __init__(self, *args, **kwargs):
        self.parser = ArgumentParser(*args, **kwargs)
        self.subparsers = None
        self.func = None


    @property
    def subcommand(self):
        if self.subparsers is None:
            self.subparsers = self.parser.add_subparsers(
                help='Sub Commands', title='Commands', metavar='COMMAND'
            )
        return subcommand(self.subparsers)


    def __call__(self, args_or_func=None, namespace=None):

        if inspect.isroutine(args_or_func):
            self.func = args_or_func
            if self.func.__doc__ and not self.parser.description:
                self.parser.description = self.func.__doc__

            if hasattr(self.func, '__cli_args__'):
                for p_args, p_kwargs in self.func.__cli_args__:
                    self.parser.add_argument(*p_args, **p_kwargs)

            self.arg_names = add_arguments_from_func(self.func, self.parser)

            return self

        if not self.func:
            raise RuntimeError("command function must be set")



        args = self.parser.parse_args(args_or_func, namespace)

        sc_kwargs = args.__dict__.copy()
        kwargs = {}
        for k in list(sc_kwargs):
            if k in self.arg_names:
                kwargs[k] = sc_kwargs.pop(k)

        subcommand = sc_kwargs.pop('subcommand', None)

        ctx = self.func(**kwargs)

        if subcommand:
            subcommand.func(ctx, **sc_kwargs)



def arg(*args, **kwargs):
    def inner(func):
        if not hasattr(func, '__cli_args__'):
            func.__cli_args__ = []
        func.__cli_args__.append((args, kwargs))
        return func
    return inner


@command()
@arg('--y', help='This is the y arg')
def main(y=1):
    """
    This is the doc
    """

    print("Main y =", y)
    # This argument is passed to the sub_commands
    return 'binstar'


@main.subcommand
@arg('--value', type=int)
def echo(ctx, value=1):
    '''
    This is echo
    
    it is a subcommand
    '''

    print("echo", repr((ctx, value)))


@main.subcommand
def bar(ctx, what='ok'):
    '''
    This is echo
    
    it is a subcommand
    '''

    print("bar", repr((ctx, what)))


if __name__ == '__main__':
    main()

