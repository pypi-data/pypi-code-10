import click

from bitter import extractor


@click.group()
@click.option("--verbose", is_flag=True)
@click.option("--config", required=False)
def main(verbose, config):
    pass

@main.command()
@click.option('--recursive', is_flag=True, help='Get following/follower/info recursively.', default=False)
@click.option('-u', '--user', default=None)
@click.option('-d', '--dburi',show_default=True, default=None)
@click.option('-c', '--credentials',show_default=True, default='credentials.txt')
@click.option('-i', '--initfile', required=True, help='List of users to load')
@click.option('-n', '--name', show_default=True, default='extractor')
def extract(recursive, user, dburi, credentials, initfile, name):
    print(locals())
    extractor.extract(recursive=recursive,
                      user=user,
                      dburi=dburi,
                      cred_file=credentials,
                      initfile=initfile,
                      extractor_name=name)

if __name__ == '__main__':
    main()
