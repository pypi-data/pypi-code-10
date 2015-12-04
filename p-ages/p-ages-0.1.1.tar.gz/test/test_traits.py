############################################################################
# Copyright 2015 Skyscanner Ltd                                            #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License");          #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#    http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
############################################################################
import unittest

from hamcrest import assert_that, calling, raises, equal_to, ends_with

import pages

from pages.traits import Trait, evaluate_traits


class TraitsTest(unittest.TestCase):
    """
    Unit test for Traits class.
    """
    def test_is_loaded(self):
        assert_that(calling(a_malformed_trait), raises(TypeError))

    def test_str(self):
        assert_that(a_trait().__str__(), ends_with('always present'))

    def test_lazy_evaluation(self):
        traits = get_traits_with_lazy_evaluation(True)

        assert_that(evaluate_traits(traits)[0], equal_to('always true #1'))

    def test_eager_evaluation(self):
        traits = get_traits_with_lazy_evaluation(False)

        assert_that(evaluate_traits(traits)[1], equal_to('always true #2'))


def get_traits_with_lazy_evaluation(value):
        lazy_evaluated_trait = pages.traits
        lazy_evaluated_trait.__dict__['LAZY_EVALUATION'] = value

        first_trait = lazy_evaluated_trait.Trait(lambda: False, 'always true #1')
        second_trait = lazy_evaluated_trait.Trait(lambda: False, 'always true #2')
        return [first_trait, second_trait]


def foo():
    pass


def a_malformed_trait():
    return Trait(foo(), 'a non callable condition')


def a_trait():
    return Trait(lambda: True, 'always present')
