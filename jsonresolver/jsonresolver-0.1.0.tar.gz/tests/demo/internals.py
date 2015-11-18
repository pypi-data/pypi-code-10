import jsonresolver
import requests

from werkzeug.routing import Rule


@jsonresolver.hookimpl
def jsonresolver_loader(url_map):
    def endpoint(recid):
        return requests.get(
            'https://cds.cern.ch/record/{recid}?of=recjson'.format(recid=recid)
        ).json

    url_map.add(
        Rule('/record/<recid>', endpoint=endpoint, host='http://cds.cern.ch')
    )
