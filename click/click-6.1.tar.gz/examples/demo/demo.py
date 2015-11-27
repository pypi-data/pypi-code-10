import click


class VcsContext(object):

    def __init__(self):
        self.debug = False


class FancyContext(object):

    def __init__(self):
        pass


pass_vcs = click.make_pass_decorator(VcsContext, ensure=True)
pass_fancy = click.make_pass_decorator(FancyContext, ensure=True)


@click.group()
@pass_vcs
def cli(obj):
    """Write stuff here."""
    print obj


@click.group()
@pass_vcs
def commit(obj):
    """This commits some stuff."""
    print obj


@click.command()
@pass_fancy
def fancy_thing(obj):
    ctx = click.get_current_context()
    print obj
    print 'find vcs context', ctx.find_object(VcsContext)


cli.add_command(commit)
commit.add_command(fancy_thing)


if __name__ == '__main__':
    cli()
