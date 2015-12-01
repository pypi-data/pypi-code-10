# Copyright 2014 Nathan Wilcox
#
# This file is distributed under the terms of the TGPPL v. 1.0 found
# in ./COPYING.TGPPL.rst.

"""_Dim_ensional _Ana_lysis - Values with associated measurement units.

Example:
>>> from dimana import Dimana

>>> Feet = Dimana.get_dimension('Feet')
>>> Lbs = Dimana.get_dimension('Lbs')
>>> Sec = Dimana.get_dimension('Sec')
>>> Feet(23) * Lbs(13) / (Sec(1) * Sec(1))
299 [(Feet*Lbs) / Sec^2]

For values without measurement units, call the Dimana constructor directly:
>>> goldenratio = Dimana('1.6180')
>>> Feet('10.0') * goldenratio
16.18000 [Feet]
"""

from decimal import Decimal


class Dimana (object):
    # Warning: This assumes subclass names are unique across the runtime.

    @staticmethod
    def get_dimension(name):
        return Dimana._get_multi( {name: 1} )

    @staticmethod
    def _get_multi(dims):
        key = 'Dimana' + '_'.join( '%s_%s' % p for p in sorted(dims.items())).replace('-','_')

        try:
            return Dimana._subtype_cache[key]
        except KeyError:
            subtype = Dimana._define_new(key, dims)
            Dimana._subtype_cache[key] = subtype

            # Constants:
            subtype.zero = subtype('0.0')
            subtype.one = subtype('1.0')

            return subtype

    @staticmethod
    def _define_new(name, dims):
        return type(name, (Dimana,), {'_dims': dims})

    _subtype_cache = {}

    _dims = {}

    def __init__(self, value):
        self.value = Decimal(value)

    @property
    def dimstr(self):
        poses = []
        negs = []
        for (unit, power) in self._dims.iteritems():
            assert power != 0, `self._dims`
            abspower = abs(power)

            s = unit
            if abspower != 1:
                s += '^%d' % abspower

            if power > 0:
                poses.append(s)
            else:
                negs.append(s)

        posstr = '*'.join(poses)
        negstr = '*'.join(negs)
        if negs:
            if poses:
                if len(poses) > 1:
                    posstr = '(%s)' % (posstr,)
            else:
                posstr = '1'
            if len(negs) > 1:
                negstr = '(%s)' % (negstr,)

            result = '%s / %s' % (posstr, negstr)
        else:
            result = posstr
        return '[%s]' % (result,)

    @property
    def inverse(self):
        """a/inverse has value (1/a.value) and inverse units."""
        return self.inverseunits( Decimal(1) / self.value )

    @property
    def inverseunits(self):
        return type(self)._get_multi(dict( (k, -v) for (k, v) in self._dims.iteritems() ))

    def __repr__(self):
        return '%s %s' % (self.value, self.dimstr)

    def __cmp__(self, other):
        typecheck(other, type(self))
        return cmp(self.value, other.value)

    def __add__(self, other):
        """Returns a Dimana with a .value of a.value + b.value

        Precondition: a and b must be the same type with identical
        units or else a TypeError is raised.
        """
        typecheck(other, type(self))
        return type(self)(self.value + other.value)

    def __sub__(self, other):
        """Defined as: a + (- b)"""
        return self + ( - other )

    def __neg__(self):
        """return -a which has identical units as a and a value of -(a.value)."""
        return type(self)( - self.value )

    def __mul__(self, other):
        """return (a*b) with value (a.value * b.value) and unit dimensions the sum of a and b.

        Preconditions: a and b must be the same type (notably not other
        python numeric types).

        Note: In order to multiply by a dimensionless quanitity, use the Dimana
        constructor directly:

        >>> Feet = Dimana.get_dimensions('Feet')
        >>> length = Feet('10.0')
        >>> goldenratio = Dimana('1.6180')
        >>> length * goldenratio
        16.18000 [Feet]
        """
        typecheck(other, Dimana)

        dims={}
        for key in set(self._dims.keys() + other._dims.keys()):
            sumpower = self._dims.get(key, 0) + other._dims.get(key, 0)
            if sumpower != 0:
                dims[key] = sumpower

        cls = Dimana._get_multi(dims)
        return cls(self.value * other.value)

    def __pow__(self, p):
        """return a**p with value (a.value ** p) and unit dimensions multiplied by p.

        preconditions: p must be an int, or float, not a Dimana.

        DOC BUG: Can p be a Decimal? -add a unit test.
        """
        if p == 1.0:
            return self
        elif p == 0:
            # NOTE: Without this special case, Decimal('0') ** 0 raises an exception.
            return Dimana.one
        else:
            dims={}
            for (unit, power) in self._dims.items():
                powerpower = power * p
                if powerpower != 0:
                    dims[unit] = powerpower

            cls = Dimana._get_multi(dims)
            return cls(self.value ** p)

    def __div__(self, other):
        """(a / b) is defined as (a * b.inverse)"""
        return self * other.inverse

Dimana.zero = Dimana('0.0')
Dimana.one = Dimana('1.0')


def typecheck(i, t):
    if not isinstance(i, t):
        raise TypeError('Type %r does not include instance %r' % (t, i))

