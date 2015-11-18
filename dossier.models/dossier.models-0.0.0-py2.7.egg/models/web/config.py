from __future__ import absolute_import, division, print_function

from gensim import models

from dossier.models.openquery.google import Google
from dossier.akagraph import AKAGraph
import dossier.web as web


class Config(web.Config):
    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)
        self._tfidf = None

    @property
    def config_name(self):
        return 'dossier.models'

    def normalize_config(self, config):
        super(Config, self).normalize_config(config)
        try:
            tfidf_path = self.config['tfidf_path']
        except KeyError:
            self._tfidf = False  # service available but absent
        else:
            self._tfidf = models.TfidfModel.load(tfidf_path)

        akagraph_config = self.config.get('akagraph')
        if akagraph_config:
            self._akagraph = AKAGraph(akagraph_config['hosts'], akagraph_config['index_name'])
        else:
            self._akagraph = None

    @property
    def tfidf(self):
        return self._tfidf

    @property
    def akagraph(self):
        return self._akagraph

    @property
    def google(self):
        api_key = self.config.get('google_api_search_key')
        if api_key is None:
            return None
        return Google(api_key)
