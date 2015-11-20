"""Migration script to import DCAT vocabularies"""
from __future__ import print_function
from os.path import join, dirname

from cubes.skos.dataimport import SimpleImportLog
from cubes.skos.sobjects import _skos_import_rdf


def datapath(fname):
    return join(dirname(__file__), 'data', fname)


def rdf_import(url):
    import_log = SimpleImportLog(url)
    stats, concept_schemes = _skos_import_rdf(session, url, import_log, raise_on_error=True)
    commit(ask_confirm=False)
    return len(stats[0]), concept_schemes


for name, fname in [
    ('ADMS vocabularies', 'ADMS_SKOS_v1.00.rdf'),
    ('Dublin Core Collection Description Terms', 'cldterms.rdf'),
    ('Dublin Core Collection Description Frequency', 'freq.rdf')
]:
    print('-> importing ' + name)
    ncreated, schemes = rdf_import(datapath(fname))
    print('   {0} entities imported (incl. {1} concept schemes)'.format(
        ncreated, len(schemes)))
