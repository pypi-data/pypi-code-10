from __future__ import print_function

import functools
from parseratorvariable import ParseratorType, consolidate
import probablepeople
from .gender import gender_names
from .frequency import given_name_freq, surname_freq
import numpy

PERSON = (('marital prefix',      ('PrefixMarital',)),
          ('given name',          ('GivenName',
                                   'FirstInitial')),
          ('middle name',         ('MiddleName',
                                   'MiddleInitial')),
          ('surname',             ('Surname',
                                   'LastInitial')),
          ('generational suffix', ('SuffixGenerational',)),
          ('other prefix',        ('PrefixOther',)),
          ('other suffix',        ('SuffixOther',)),
          ('nick name',           ('NickName',)),
          ('gender',              ('Gender',)),
          ('has generational suffix', ('HasSuffixGenerational')),
          ('probality given name', ('FreqGivenName',)),
          ('probality surname', ('FreqSurName',)),
          ('given name probability interaction', ('FreqInteractionGivenName',)),
          ('surname probability interaction', ('FreqInteractionSurName',)))




FIRST_NAMES_A = (('marital prefix A',      ('PrefixMarital')),
                 ('given name A',          ('GivenName',
                                            'FirstInitial')),
                 ('middle name A',         ('MiddleName',
                                            'MiddleInitial')),
                 ('other prefix A',        ('PrefixOther',)),
                 ('nick name A',           ('NickName',)))

LAST_NAMES_A = (('surname A',             ('Surname',
                                          'LastInitial')),
                ('generational suffix A', ('SuffixGenerational',)),
                ('other suffix A',        ('SuffixOther',)))

FIRST_NAMES_B = (('marital prefix B',      ('SecondPrefixMarital',)),
                 ('given name B',          ('SecondGivenName',
                                            'SecondFirstInitial')),
                 ('middle name B',         ('SecondMiddleName',
                                            'SecondMiddleInitial')),
                 ('other prefix B',        ('SecondPrefixOther',)),
                 ('nick name B',           ('SecondNickName',)))

LAST_NAMES_B = (('surname B',             ('SecondSurname',
                                           'SecondLastInitial')),
                ('generational suffix B', ('SecondSuffixGenerational',)),
                ('other suffix B',        ('SecondSuffixOther',)))

CORPORATION = (('corporation name',         ('CorporationName', 'ShortForm')),
               ('corporation org',          ('CorporationNameOrganization',)),
               ('corporation type',         ('CorporationLegalType',)),
               ('client corporation name',  ('ProxiedCorporationName', 
                                             'ProxiedShortForm')),
               ('client corporation org',   ('ProxiedCorporationNameOrganization',)),
               ('client corporation type',  ('ProxiedCorporationLegalType',)))


_, FIRST_NAMES_A_PARTS = list(zip(*FIRST_NAMES_A))
_, FIRST_NAMES_B_PARTS = list(zip(*FIRST_NAMES_B))
_, LAST_NAMES_A_PARTS = list(zip(*LAST_NAMES_A))

COMBO_NAMES = len(FIRST_NAMES_A) + len(LAST_NAMES_A)

FIRST_NAME_PLACES = numpy.array([False] * (COMBO_NAMES * 2))
FIRST_NAME_PLACES[0:len(FIRST_NAMES_A)] = True
FIRST_NAME_PLACES[COMBO_NAMES:COMBO_NAMES+len(FIRST_NAMES_A)] = True


class WesternNameType(ParseratorType) :
    type = "Name"

    def __init__(self, definition) :
        self.components = (('Person' , self.compareFields, PERSON),
                           ('Corporation', self.compareFields, CORPORATION),
                           ('Household', self.compareHouseholds, 
                            FIRST_NAMES_A + LAST_NAMES_A,
                            FIRST_NAMES_B + LAST_NAMES_B))

        super(WesternNameType, self).__init__(definition)

    @staticmethod
    def tagger(field) :
        tags, name_type = probablepeople.tag(field)
        tags['Gender'] = gender_names.get(tags.get('GivenName', None), 
                                          numpy.nan)
        tags['HasSuffixGenerational'] = tags.get('SuffixGenerational', None)
        tags['FreqGivenName'] = given_name_freq.get(tags.get('GivenName',
                                                             None),
                                                    numpy.nan)
        tags['FreqSurName'] = given_name_freq.get(tags.get('SurName',
                                                             None),
                                                    numpy.nan)
        tags['FreqInteractionGivenName'] = None
        tags['FreqInteractionSurName'] = None

        return tags, name_type


    def compareHouseholds(self, tags_a, tags_b, field_1, field_2) :
        all_tags = set().union(field_1.keys(), field_2.keys())

        if {'SecondSurname', 'SecondLastInitial'} & all_tags :
            return self.comparePermutable(tags_a, tags_b, field_1, field_2)

        else :
            distances = numpy.empty(len(tags_a) * 2)
            distances[:] = numpy.nan

            first_name_dist = self.comparePermutable(FIRST_NAMES_A_PARTS,
                                                     FIRST_NAMES_B_PARTS,
                                                     field_1,
                                                     field_2)
            distances[FIRST_NAME_PLACES] = first_name_dist

            last_name_dist = list(self.compareFields(LAST_NAMES_A_PARTS,
                                                     field_1,
                                                     field_2))
            distances[len(FIRST_NAMES_A) : COMBO_NAMES] = last_name_dist

            return distances

    def compareFields(self, parts, field_1, field_2) :
        surname_dist = given_name_dist = numpy.nan
        joinParts = functools.partial(consolidate, components=parts)   
        for part, (part_1, part_2) in zip(parts, zip(*map(joinParts, [field_1, field_2]))) :
            if part == ('Gender',) :
                yield part_1 + part_2 - 2 * part_1 * part_2
            elif part == ('GivenName', 'FirstInitial') :
                given_name_dist = self.compareString(part_1, part_2)
                yield given_name_dist
            elif part == ('SurName', 'LastInitial') :
                surname_dist = self.compareString(part_1, part_2)
                yield surname_dist
            elif part == ('FreqGivenName',) :
                prob_given_name = part_1 * part_2
                yield prob_given_name
            elif part == ('FreqSurName',) :
                prob_surname = part_1 * part_2
                yield prob_surname
            elif part == ('FreqInteractionGivenName',) :
                yield prob_given_name * given_name_dist
            elif part == ('FreqInteractionSurName',) :
                yield prob_surname * surname_dist
            elif part == ('HasSuffixGenerational',) :
                if bool(part_1) != bool(part_2) : # exclusive or
                    yield 1.0
                else :
                    yield 0.0
            elif part in {('CorporationName', 'ShortForm'),
                          ('OtherCorporationName', 'OtherShortForm'),
                          ('ProxiedCorporationName', 'ProxiedShortForm')} :
                remainder_1 = part_1.split('the ', 1)[-1]
                remainder_2 = part_2.split('the ', 1)[-1]
                yield self.compareString(remainder_1, remainder_2)
            else :
                yield self.compareString(part_1, part_2)
