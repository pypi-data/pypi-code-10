import click
import run as crun
import log as clog
import server as cserver

description = """
Monitor and log your crontasks
"""

example = """
examples:
    your-script.sh arguments | cronmon -l ~/cronmon your-project
    conrmon -c "your-script.sh arguments" your-project
    cronmon -c "script.sh" -l ~/cronmon -f "fail-script.sh"
"""


@click.group()
def cli():
    """
    Monitor and log your crontasks

    examples:
        your-script.sh arguments | cronmon -l ~/cronmon your-project
        conrmon -c "your-script.sh arguments" your-project
    """
    pass


@cli.command()
@click.option('-c', '--command', help='Command to execute', required=False, default=None)
@click.option('-l', '--location', help='Directory where logfiles will be store', required=True)
@click.option('-f', '--on-fail', help='When failing run', required=False, default=None)
@click.argument('name')
def run(command, location, on_fail, name):
    crun.start(command, location, on_fail, name)


@cli.command()
@click.option('-n', '--number', help='Number of log to show', required=False, default=None)
@click.option(
    '-l', '--location', help='Directory where logfiles will be store',
    required=False, default="~/cronmon")
@click.argument('name')
def log(number, name):
    clog.start(name, number)


@cli.command()
@click.option('-p', '--port', help='Port number', required=False, default=5000)
@click.option('-l', '--location', help='Directory where logfiles are stored', required=True)
def server(port, location):
    cserver.start(port, location)


def main():
    cli()


if __name__ == '__main__':
    print(__doc__)
