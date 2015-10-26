# Authors: Lukas Breuer <l.breuer@fz-juelich.de>
#          Juergen Dammers <j.dammers@fz-juelich.de>
#          Denis A. Engeman <denis.engemann@gemail.com>
#
# License: BSD (3-clause)

import math

import numpy as np

from ..utils import logger, verbose, check_random_state, random_permutation


@verbose
def infomax(data, weights=None, l_rate=None, block=None, w_change=1e-12,
            anneal_deg=60., anneal_step=0.9, extended=False, n_subgauss=1,
            kurt_size=6000, ext_blocks=1, max_iter=200,
            random_state=None, blowup=1e4, blowup_fac=0.5, n_small_angle=20,
            use_bias=True, verbose=None):
    """Run the (extended) Infomax ICA decomposition on raw data

    based on the publications of Bell & Sejnowski 1995 (Infomax)
    and Lee, Girolami & Sejnowski, 1999 (extended Infomax)

    Parameters
    ----------
    data : np.ndarray, shape (n_samples, n_features)
        The data to unmix.
    w_init : np.ndarray, shape (n_features, n_features)
        The initialized unmixing matrix. Defaults to None. If None, the
        identity matrix is used.
    l_rate : float
        This quantity indicates the relative size of the change in weights.
        Note. Smaller learining rates will slow down the procedure.
        Defaults to 0.010d / alog(n_features ^ 2.0)
    block : int
        The block size of randomly chosen data segment.
        Defaults to floor(sqrt(n_times / 3d))
    w_change : float
        The change at which to stop iteration. Defaults to 1e-12.
    anneal_deg : float
        The angle at which (in degree) the learning rate will be reduced.
        Defaults to 60.0
    anneal_step : float
        The factor by which the learning rate will be reduced once
        ``anneal_deg`` is exceeded:
            l_rate *= anneal_step
        Defaults to 0.9
    extended : bool
        Wheather to use the extended infomax algorithm or not. Defaults to
        True.
    n_subgauss : int
        The number of subgaussian components. Only considered for extended
        Infomax.
    kurt_size : int
        The window size for kurtosis estimation. Only considered for extended
        Infomax.
    ext_blocks : int
        Only considered for extended Infomax.
        If positive, it denotes the number of blocks after which to recompute
        the Kurtosis, which is used to estimate the signs of the sources.
        In this case the number of sub-gaussian sources is automatically
        determined.
        If negative, the number of sub-gaussian sources to be used is fixed
        and equal to n_subgauss. In this case the Kurtosis is not estimated.
    max_iter : int
        The maximum number of iterations. Defaults to 200.
    random_state : int | np.random.RandomState
        If random_state is an int, use random_state as seed of the random
        number generator.
        If random_state is already a np.random.RandomState instance, use
        random_state as random number generator.
    blowup : float
        The maximum difference allowed between two succesive estimations of the
        unmixing matrix. Defaults to 1e4
    blowup_fac : float
        The factor by which the learning rate will be reduced if the
        difference between two succesive estimations of the
        unmixing matrix exceededs ``blowup``:
            l_rate *= blowup_fac
        Defaults to 0.5
    n_small_angle : int | None
        The maximum number of allowed steps in which the angle between two
        succesive estimations of the unmixing matrix is less than
        ``anneal_deg``.
        If None, this parameter is not taken into account to stop the
        iterations.
        Defaults to 20
    use_bias : bool
        This quantity indicates if the bias should be computed.
        Defaults to True
    verbose : bool, str, int, or None
        If not None, override default verbose level (see mne.verbose).

    Returns
    -------
    unmixing_matrix : np.ndarray of float, shape (n_features, n_features)
        The linear unmixing operator.
    """
    from scipy.stats import kurtosis
    rng = check_random_state(random_state)

    # define some default parameter
    max_weight = 1e8
    restart_fac = 0.9
    min_l_rate = 1e-10
    degconst = 180.0 / np.pi

    # for extended Infomax
    extmomentum = 0.5
    signsbias = 0.02
    signcount_threshold = 25
    signcount_step = 2

    # check data shape
    n_samples, n_features = data.shape
    n_features_square = n_features ** 2

    # check input parameter
    # heuristic default - may need adjustment for
    # large or tiny data sets
    if l_rate is None:
        l_rate = 0.01 / math.log(n_features ** 2.0)

    if block is None:
        block = int(math.floor(math.sqrt(n_samples / 3.0)))

    logger.info('computing%sInfomax ICA' % ' Extended ' if extended is True
                else ' ')

    # collect parameter
    nblock = n_samples // block
    lastt = (nblock - 1) * block + 1

    # initialize training
    if weights is None:
        # initialize weights as identity matrix
        weights = np.identity(n_features, dtype=np.float64)

    BI = block * np.identity(n_features, dtype=np.float64)
    bias = np.zeros((n_features, 1), dtype=np.float64)
    onesrow = np.ones((1, block), dtype=np.float64)
    startweights = weights.copy()
    oldweights = startweights.copy()
    step = 0
    count_small_angle = 0
    wts_blowup = False
    blockno = 0
    signcount = 0
    initial_ext_blocks = ext_blocks   # save the initial value in case of reset

    # for extended Infomax
    if extended is True:
        signs = np.ones(n_features)

        for k in range(n_subgauss):
            signs[k] = -1

        kurt_size = min(kurt_size, n_samples)
        old_kurt = np.zeros(n_features, dtype=np.float64)
        oldsigns = np.zeros(n_features)

    # trainings loop
    olddelta, oldchange = 1., 0.
    while step < max_iter:

        # shuffle data at each step
        permute = random_permutation(n_samples, rng)

        # ICA training block
        # loop across block samples
        for t in range(0, lastt, block):
            u = np.dot(data[permute[t:t + block], :], weights)
            u += np.dot(bias, onesrow).T

            if extended is True:
                # extended ICA update
                y = np.tanh(u)
                weights += l_rate * np.dot(weights,
                                           BI -
                                           signs[None, :] * np.dot(u.T, y) -
                                           np.dot(u.T, u))
                if use_bias:
                    bias += l_rate * np.reshape(np.sum(y, axis=0,
                                                dtype=np.float64) * -2.0,
                                                (n_features, 1))

            else:
                # logistic ICA weights update
                y = 1.0 / (1.0 + np.exp(-u))
                weights += l_rate * np.dot(weights,
                                           BI + np.dot(u.T, (1.0 - 2.0 * y)))

                if use_bias:
                    bias += l_rate * np.reshape(np.sum((1.0 - 2.0 * y), axis=0,
                                                dtype=np.float64),
                                                (n_features, 1))

            # check change limit
            max_weight_val = np.max(np.abs(weights))
            if max_weight_val > max_weight:
                wts_blowup = True

            blockno += 1
            if wts_blowup:
                break

            # ICA kurtosis estimation
            if extended is True:

                if ext_blocks > 0 and blockno % ext_blocks == 0:

                    if kurt_size < n_samples:
                        rp = np.floor(rng.uniform(0, 1, kurt_size) *
                                      (n_samples - 1))
                        tpartact = np.dot(data[rp.astype(int), :], weights).T
                    else:
                        tpartact = np.dot(data, weights).T

                    # estimate kurtosis
                    kurt = kurtosis(tpartact, axis=1, fisher=True)

                    if extmomentum != 0:
                        kurt = (extmomentum * old_kurt +
                                (1.0 - extmomentum) * kurt)
                        old_kurt = kurt

                    # estimate weighted signs
                    signs = np.sign(kurt + signsbias)

                    ndiff = (signs - oldsigns != 0).sum()
                    if ndiff == 0:
                        signcount += 1
                    else:
                        signcount = 0
                    oldsigns = signs

                    if signcount >= signcount_threshold:
                        ext_blocks = np.fix(ext_blocks * signcount_step)
                        signcount = 0

        # here we continue after the for
        # loop over the ICA training blocks
        # if weights in bounds:
        if not wts_blowup:
            oldwtchange = weights - oldweights
            step += 1
            angledelta = 0.0
            delta = oldwtchange.reshape(1, n_features_square)
            change = np.sum(delta * delta, dtype=np.float64)
            if step > 2:
                angledelta = math.acos(np.sum(delta * olddelta) /
                                       math.sqrt(change * oldchange))
                angledelta *= degconst

            if verbose:
                logger.info(
                    'step %d - lrate %5f, wchange %8.8f, angledelta %4.1f deg'
                    % (step, l_rate, change, angledelta))

            # anneal learning rate
            oldweights = weights.copy()
            if angledelta > anneal_deg:
                l_rate *= anneal_step    # anneal learning rate
                # accumulate angledelta until anneal_deg reached l_rates
                olddelta = delta
                oldchange = change
                count_small_angle = 0  # reset count when angle delta is large
            else:
                if step == 1:  # on first step only
                    olddelta = delta  # initialize
                    oldchange = change

                if n_small_angle is not None:
                    count_small_angle += 1
                    if count_small_angle > n_small_angle:
                        max_iter = step

            # apply stopping rule
            if step > 2 and change < w_change:
                step = max_iter
            elif change > blowup:
                l_rate *= blowup_fac

        # restart if weights blow up
        # (for lowering l_rate)
        else:
            step = 0  # start again
            wts_blowup = 0  # re-initialize variables
            blockno = 1
            l_rate *= restart_fac  # with lower learning rate
            weights = startweights.copy()
            oldweights = startweights.copy()
            olddelta = np.zeros((1, n_features_square), dtype=np.float64)
            bias = np.zeros((n_features, 1), dtype=np.float64)

            ext_blocks = initial_ext_blocks

            # for extended Infomax
            if extended:
                signs = np.ones(n_features)
                for k in range(n_subgauss):
                    signs[k] = -1
                oldsigns = np.zeros(n_features)

            if l_rate > min_l_rate:
                if verbose:
                    logger.info('... lowering learning rate to %g'
                                '\n... re-starting...' % l_rate)
            else:
                raise ValueError('Error in Infomax ICA: unmixing_matrix matrix'
                                 'might not be invertible!')

    # prepare return values
    return weights.T
