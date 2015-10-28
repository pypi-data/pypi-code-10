"""
problog.sdd_formula - Sentential Decision Diagrams
--------------------------------------------------

Interface to Sentential Decision Diagrams (SDD)

..
    Part of the ProbLog distribution.

    Copyright 2015 KU Leuven, DTAI Research Group

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
from __future__ import print_function

from .formula import LogicDAG
from .core import transform
from .errors import InstallError
from .dd_formula import DD, build_dd, DDManager


# noinspection PyBroadException
try:
    import sdd
except Exception:
    sdd = None


class SDD(DD):
    """A propositional logic formula consisting of and, or, not and atoms represented as an SDD.

    This class has two restrictions with respect to the default LogicFormula:

        * The number of atoms in the SDD should be known at construction time.
        * It does not support updatable nodes.

    This means that this class can not be used directly during grounding.
    It can be used as a target for the ``makeAcyclic`` method.
    """

    transform_preference = 10

    def __init__(self, sdd_auto_gc=False, **kwdargs):
        if sdd is None:
            raise InstallError('The SDD library is not available. Please run the installer.')
        self.auto_gc = sdd_auto_gc
        DD.__init__(self, auto_compact=False, **kwdargs)

    def _create_manager(self):
        return SDDManager(auto_gc=self.auto_gc)

    @classmethod
    def is_available(cls):
        """Checks whether the SDD library is available."""
        return sdd is not None


class SDDManager(DDManager):
    """
    Manager for SDDs.
    It wraps around the SDD library and offers some additional methods.
    """

    def __init__(self, varcount=0, auto_gc=True):
        """Create a new SDD manager.

        :param varcount: number of initial variables
        :type varcount: int
        :param auto_gc: use automatic garbage collection and minimization
        :type auto_gc: bool
        """
        DDManager.__init__(self)
        if varcount is None or varcount == 0:
            varcount = 1
        self.__manager = sdd.sdd_manager_create(varcount, auto_gc)
        self.varcount = varcount

    def get_manager(self):
        """Get the underlying sdd manager."""
        return self.__manager

    def add_variable(self, label=0):
        if label == 0 or label > self.varcount:
            sdd.sdd_manager_add_var_after_last(self.__manager)
            self.varcount += 1
            return self.varcount
        else:
            return label

    def literal(self, label):
        self.add_variable(abs(label))
        return sdd.sdd_manager_literal(label, self.__manager)

    def is_true(self, node):
        return sdd.sdd_node_is_true(node)

    def true(self):
        return sdd.sdd_manager_true(self.__manager)

    def is_false(self, node):
        return sdd.sdd_node_is_false(node)

    def false(self):
        return sdd.sdd_manager_false(self.__manager)

    def conjoin2(self, a, b):
        return sdd.sdd_conjoin(a, b, self.__manager)

    def disjoin2(self, a, b):
        return sdd.sdd_disjoin(a, b, self.__manager)

    def negate(self, node):
        new_sdd = sdd.sdd_negate(node, self.__manager)
        self.ref(new_sdd)
        return new_sdd

    def same(self, node1, node2):
        # Assumes SDD library always reuses equivalent nodes.
        if node1 is None or node2 is None:
            return node1 == node2
        else:
            return int(node1) == int(node2)

    def ref(self, *nodes):
        for node in nodes:
            sdd.sdd_ref(node, self.__manager)

    def deref(self, *nodes):
        for node in nodes:
            sdd.sdd_deref(node, self.__manager)

    def write_to_dot(self, node, filename):
        sdd.sdd_save_as_dot(filename, node)

    def wmc(self, node, weights, semiring):
        logspace = 0
        if semiring.one() == 0.0:
            logspace = 1
        wmc_manager = sdd.wmc_manager_new(node, logspace, self.get_manager())
        varcount = sdd.sdd_manager_var_count(self.get_manager())

        # varlist_intern = sdd.sdd_variables(node, self.get_manager())
        # vc = sdd.sdd_manager_var_count(self.get_manager()) + 1
        # varlist = [i for i in range(0, vc) if sdd.sdd_array_int_element(varlist_intern, i)]

        for n in weights:
            pos, neg = weights[n]
            if n <= varcount:
                sdd.wmc_set_literal_weight(n, pos, wmc_manager)  # Set positive literal weight
                sdd.wmc_set_literal_weight(-n, neg, wmc_manager)  # Set negative literal weight
        result = sdd.wmc_propagate(wmc_manager)
        sdd.wmc_manager_free(wmc_manager)
        return result

    def wmc_literal(self, node, weights, semiring, literal):
        logspace = 0
        if semiring.one() == 0.0:
            logspace = 1
        wmc_manager = sdd.wmc_manager_new(node, logspace, self.get_manager())
        varcount = sdd.sdd_manager_var_count(self.get_manager())
        for i, n in enumerate(sorted(weights)):
            i += 1
            pos, neg = weights[n]
            if n <= varcount:
                sdd.wmc_set_literal_weight(n, pos, wmc_manager)  # Set positive literal weight
                sdd.wmc_set_literal_weight(-n, neg, wmc_manager)  # Set negative literal weight
        sdd.wmc_propagate(wmc_manager)

        result = sdd.wmc_literal_pr(literal, wmc_manager)
        sdd.wmc_manager_free(wmc_manager)
        return result

    def wmc_true(self, weights, semiring):
        logspace = 0
        if semiring.one() == 0.0:
            logspace = 1
        wmc_manager = sdd.wmc_manager_new(self.true(), logspace, self.get_manager())
        varcount = sdd.sdd_manager_var_count(self.get_manager())
        for i, n in enumerate(sorted(weights)):
            i += 1
            pos, neg = weights[n]
            if n <= varcount:
                sdd.wmc_set_literal_weight(n, pos, wmc_manager)  # Set positive literal weight
                sdd.wmc_set_literal_weight(-n, neg, wmc_manager)  # Set negative literal weight
        result = sdd.wmc_propagate(wmc_manager)
        sdd.wmc_manager_free(wmc_manager)
        return result

    def __del__(self):
        sdd.sdd_manager_free(self.__manager)
        self.__manager = None


@transform(LogicDAG, SDD)
def build_sdd(source, destination, **kwdargs):
    """Build an SDD from another formula.

    :param source: source formula
    :param destination: destination formula
    :param kwdargs: extra arguments
    :return: destination
    """
    return build_dd(source, destination, **kwdargs)
