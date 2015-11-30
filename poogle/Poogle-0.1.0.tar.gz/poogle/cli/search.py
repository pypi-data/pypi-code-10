import re

import click

from poogle import google_search
from poogle.cli import pass_context, Context


@click.command('search')
@click.argument('query')
@click.option('-r', '--results', help='The number of search results to retrieve', default=10)
@click.option('--plain', help='Disables bolding and keyword highlighting', is_flag=True)
@pass_context
def cli(ctx, query, results, plain):
    """
    Execute a Google search query and display the results
    """
    assert isinstance(ctx, Context)

    # Execute our search query
    click.echo('Executing search query for {q}\n'.format(q=click.style(query, 'blue', bold=True)))
    results = google_search(query, results)

    # Split our query parts for highlighting
    query_parts = query.split()

    for result in results:
        # Formatted results
        if not plain:
            title = click.style(result.title, bold=True)
            for part in query_parts:
                ctx.log.info('Parsing highlighting for query parameter %s', part)
                matches = re.findall(re.escape(part), title, re.IGNORECASE)
                if not matches:
                    continue

                matches = set(matches)
                for match in matches:
                    highlighted = click.style(match, 'blue', bold=True)
                    title = title.replace(match, highlighted + click.style('', bold=True, reset=False))

            click.secho(title)
            click.secho('=' * 30)
            click.secho(result.url.as_string())
        else:
            click.echo(result.title)
            click.echo('=' * 30)
            click.echo(result.url.as_string())

        click.echo()
