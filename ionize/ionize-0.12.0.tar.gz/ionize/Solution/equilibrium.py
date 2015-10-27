import numpy as np
from math import log10, sqrt
from scipy.optimize import newton, brentq
import warnings


def calculate_ionic_strength(self, pH, guess):
    # For each ion, add the contribution to ionic strength to the sum.

    I = sum([self.concentration(ion) *
             np.sum(ion.valence**2 *
                    ion.ionization_fraction(pH, guess))
             for ion in self.ions]) / 2.

    # Add the ionic strength due to water dissociation.
    I += (self.cH(pH, guess) + self.cOH(pH, guess))/2
    return I


def calculate_pH(self, ionic_strength):
    """Return the pH of the object.

    If an ionic strength is specified, uses the corrected acidity constants.
    This function should be used only when finding the equilibrium state.
    After that, the value should be pulled from obj.pH.

    If ionic strength does not exist, assume it is zero.
    This function is used to find the equilibrium state,
    so it cannot pull the ionic strength from the object.
    """
    # Find the order of the polynomial. This is the maximum
    # size of the list of charge states in an ion.
    max_columns = max([max(ion.valence)-min(ion.valence)+2
                       for ion in self.ions])
    n_ions = len(self.ions)

    # Set up the matrix of Ls, the multiplication
    # of acidity coefficients for each ion.
    l_matrix = np.array([np.resize(ion.acidity_product(ionic_strength),
                                         [max_columns])
                         for ion in self.ions])

    # Construct Q vector.
    Q = 1.0
    for j in range(n_ions):
        Q = np.convolve(Q, l_matrix[j, :])

    # Convolve with water dissociation.
    Q = np.convolve(Q, [-self.effective_dissociation(ionic_strength),
                           0.0, 1.0])


    # Construct P matrix
    PMat = []
    for i in range(n_ions):
        z_list = np.resize(self.ions[i]._valence_zero(), [max_columns])

        Mmod = l_matrix.copy()
        Mmod[i, :] *= np.array(z_list)

        Pi = 1.
        for kl in range(n_ions):
            Pi = np.convolve(Pi, Mmod[kl, :])

        Pi = np.convolve([0.0, 1.0], Pi)  # Convolve with P2
        PMat.append(Pi)

    # Multiply P matrix by concentrations, and sum.
    P = np.sum(np.array(PMat, ndmin=2) *
                  np.array(self.concentrations)[:, np.newaxis], 0)
    # Construct polynomial. Change the shapes as needed, then reverse the order
    if len(P) < len(Q):
        P.resize(Q.shape)
    elif len(P) > len(Q):
        Q.resize(P.shape)
    poly = (P+Q)[::-1]

    # Solve Polynomial for concentration

    cH = np.roots(poly)

    # Parse the real roots of the root finding algorithms
    cH = [c for c in cH if c.real > 0 and c.imag == 0]
    if len(cH) == 1:
        cH = np.real(cH)[0]
    elif len(cH) > 1:
        warnings.warn('Found multiple possible pH solutions. Choosing one.')
        cH = np.real(cH)[0]
    else:
        raise RuntimeError('Failed to find pH.')

    # Convert to pH. Use the activity to correct the calculation.
    pH = -log10(cH * self._hydronium.activity([1], ionic_strength)[0])
    return pH


def equilibrium_offset(I_i, self):
    """Return the error in ionic strength.

    Takes an ionic strength, then uses it to calculate a new ionic strength
    using the new equilibrum coefficents. find_equilibrium finds the root of
    this function.
    """
    pH = calculate_pH(self, I_i)
    I_f = calculate_ionic_strength(self, pH, I_i)

    res = (I_f-I_i)
    return res


def _equilibrate(self):
    """Return the equilibrium ionic strength and pH.

    Uses the newton's method root finder from scipy.optimize to find the
    equilibrium pH and ionic strength of a solution, using the ionic-strength
    adjusted activity coefficients. This function is called when the selfect is
    initialized.
    """

    if not self.ions:
        self._pH = -log10(sqrt(effective_dissociation(self)))
        self._ionic_strength = calculate_ionic_strength(self, self.pH, 0)
        return

    # Generate an initial ionic strength guess without activity corrections
    I = calculate_ionic_strength(self, calculate_pH(self, 0), 0)

    # Try to bound the true answer.
    b1 = equilibrium_offset(0., self)
    b2 = equilibrium_offset(2.*I, self)

    # If the answer is in the bound, use brentq. Otherwise, use newton.
    # If brentq doesn't converge, use newton.
    try:
        assert ((b1 < 0.) ^ (b2 < 0.))
        I, r = brentq(equilibrium_offset, 0, 2*I,
                      args=(self,), full_output=True)
        assert r.converged

    except AssertionError:
        I = calculate_ionic_strength(self, calculate_pH(self, 0), 0)
        I = newton(equilibrium_offset, I, args=(self,))
        warnings.warn('Couldn\'t use the brentq method. Using newton.')

    # Use this final ionic strength to find the correct pH.
    pH = calculate_pH(self, I)

    if I > 1.:
        warnings.warn(('Ionic strength > 1M. '
                      'Ionic stregth correction may be inaccurate.'))

    self._pH = pH
    self._ionic_strength = I


def effective_dissociation(self, ionic_strength=None):
    """Return the effective water dissociation constant.

    Based on the activity corrections to H+ and OH-.
    """
    if not ionic_strength:
        ionic_strength = self.ionic_strength

    gam_h = self._hydronium.activity(1, ionic_strength=ionic_strength)
    Kw_eff = self._solvent.dissociation(self.temperature())/gam_h**2
    return Kw_eff


def equilibrate_CO2(self):
    raise NotImplementedError
