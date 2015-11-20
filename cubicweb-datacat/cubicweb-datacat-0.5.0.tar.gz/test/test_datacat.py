# copyright 2014 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-datacat automatic tests"""

from cubicweb.devtools import testlib


class AutomaticWebTest(testlib.AutomaticWebTest):
    '''provides `to_test_etypes` and/or `list_startup_views` implementation
    to limit test scope
    '''

    def to_test_etypes(self):
        '''only test views for entities of the returned types'''
        return set(('Dataset', 'File', 'Script',
                    'DataTransformationProcess', 'DataValidationProcess'))


class VocabularyImportTC(testlib.CubicWebTC):
    """Functional tests ensuring concept schemes got properly imported.
    """

    def test_adms(self):
        scheme_names = (
            'assettype',
            'interoperabilitylevel',
            'licencetype',
            'publishertype',
            'representationtechnique',
            'status',
        )
        with self.admin_access.repo_cnx() as cnx:
            rset = cnx.execute(
                'Any X WHERE X is ConceptScheme, X cwuri IN ({0})'.format(
                    ','.join('"http://purl.org/adms/{0}/1.0"'.format(n)
                             for n in scheme_names)
                )
            )
        self.assertEqual(len(rset), len(scheme_names))

    def test_collection_terms(self):
        scheme_names = (
            'AccrualMethod',
            'AccrualPolicy',
            'CDType',
            'Frequency',
        )
        with self.admin_access.repo_cnx() as cnx:
            rset = cnx.execute(
                'Any X WHERE X is ConceptScheme, X cwuri IN ({0})'.format(
                    ','.join('"http://purl.org/cld/terms/{0}"'.format(n)
                             for n in scheme_names)
                )
            )
        self.assertEqual(len(rset), len(scheme_names))

    def test_frequency(self):
        """Concepts imported from "Dublin Core Collection Description Frequency".
        """
        with self.admin_access.repo_cnx() as cnx:
            rset = cnx.execute(
                'Any COUNT(X) WHERE X in_scheme C, C cwuri "{0}"'.format(
                    'http://purl.org/cld/terms/Frequency')
            )
        self.assertEqual(rset[0][0], 17)


if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
