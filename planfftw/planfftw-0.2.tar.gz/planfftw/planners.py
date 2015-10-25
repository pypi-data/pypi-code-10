#!usr/bin/env python
"""This module contains planner functions for fast FFT and other FFT-based
computations with pyFFTW.
"""

# Future improvements: Neater firfilter using the fft planners
#                      IIR filtering?
#                      Convolution (same as correlate just without reversing y)
#                      Pwelch

try:
    import pyfftw
    from ._pyfftw_basics import (fft, rfft, fftn, rfftn,
                                 ifft, irfft, ifftn, irfftn)
except ImportError:
    try:
        import scipy.fftpack as _
        from ._scipy_basics import (fft, rfft, fftn, rfftn,
                                    ifft, irfft, ifftn, irfftn)
    except ImportError:
        from ._numpy_basics import (fft, rfft, fftn, rfftn,
                                    ifft, irfft, ifftn, irfftn)

import numpy as np

from . import _utils


# ### Hidden functions
def _convolve(plan_x,
              plan_y,
              correlate=False,
              mode='full',
              axes=None,
              constant_x=False,
              constant_y=False,
              x_segmented=False):
    """Returns a planned function for computing the convolution of two
    sequences or arrays.

    The planner distinguishes between several different use cases:

        1. 1-D convolution of 1-D sequences or along single axis in N-D arrays
        2. M-D convolution of N-D sequences
        3. 1-D convolution along single axis in N-D array with 1-D sequence
        4. 1-D convolution of 1-D sequence along single axis in N-D array
        5. Special cases of 1, 2 and 3 where the first input is segmented

        The shapes of the two inputs are usually sufficient to determine which
        case should be used. However, to get 1-D convolution along single axis
        in N-D arrays, 'axes' must be a single integer or a length 1 sequence.
        In addition, x_segmented must be True for case 5.

    Parameters
    ----------
        plan_x : integer, shape or array-like
            First input sequence, it's shape or length.
        plan_y : integer, shape or array-like
            Second input sequence, it's shape or length.
        correlate : Optional[bool]
            Indicates that correlation, rather than convolution, should be
            planned. Default is False.
        mode : Optional[str]
            A string indicating the output size.

            'full'
                The output is the full discrete linear convolution of the
                inputs. (Default)
            'valid'
                The output consists only of those elements that do not rely on
                zero-padding.
            'same'
                The output is the same size as plan_x, centered with respect to
                the 'full' output.
        axes : Optional[int or sequence of ints]
            The axis or axes along which the convolution is computed.
            Default is the last N axes of the highest-rank input where N is the
            rank of the lowest-rank input.
        constant_x : Optional[boolean]
            Indicates that the first input will be constant over all uses of
            the function. If True, plan_x must be array-like.
        constant_y : Optional[boolean]
            Indicates that the second input will be constant over all uses of
            the function. If True, plan_y must be array-like.
        x_segmented : Optional[boolean]
            Indicates that the first axis of plan_x contains segments that will
            be individually used multiple times.

    Returns
    -------
        function
            Planned convolution function.

    Raises
    ------
        ValueError
            If no function can be planned for the given arguments.
    """

    # Validate arguments
    if mode not in ("valid", "same", "full"):
        raise ValueError("parameter mode must be 'valid', 'same' or 'full'.")

    # Get dimensions
    x_shape = _utils.get_shape(plan_x)
    y_shape = _utils.get_shape(plan_y)
    x_ndim = len(x_shape)
    y_ndim = len(y_shape)

    if axes is None:
        x_ndim_s = x_ndim - x_segmented
        if x_ndim_s >= y_ndim:
            from_axis = x_ndim - y_ndim
            to_axis = x_ndim
        else:
            from_axis = y_ndim - x_ndim
            to_axis = y_ndim
        axes = [k for k in range(from_axis, to_axis)]

    # Make sure axes is iterable
    if np.asarray(axes).ndim == 0:
        axes = (axes,)

    n_axes = len(axes)

    # ### Find use case
    if x_segmented:
        if x_ndim == 2 and y_ndim == 1:
            base_case = '5a'    # Correlate 1-D segments with 1-D sequences

        elif x_ndim - y_ndim == 1:
            if n_axes == 1:
                base_case = '5a'
            else:
                base_case = '5b'

        elif x_ndim > 2 and y_ndim == 1:
            base_case = '5c'

        else:
            raise ValueError("Could not plan a function with segmented x for "
                             "the given inputs.")

    elif x_ndim == 1 and y_ndim == 1:
        base_case = '1'         # Correlate 1-D sequences

    elif x_ndim == y_ndim:
        if n_axes == 1:
            base_case = '1'     # Correlate single axes in N-D sequences
        else:
            base_case = '2'     # Correlate multiple axes in N-D sequences

    elif x_ndim > 1 and y_ndim == 1:
        base_case = '3'         # Correlate single axis in N-D seq. with 1-D

        if n_axes > 1:
            raise ValueError("Cannot correlate over more axes than the least "
                             "number of dimensions in x or y.")

    elif y_ndim > 1 and x_ndim == 1:
        base_case = '4'         # Correlate 1-D seq. with single axis in N-D

        if n_axes > 1:
            raise ValueError("Cannot correlate over more axes than the least "
                             "number of dimensions in x or y.")

    else:
        raise ValueError("Could not plan a function for the given inputs.")

    if constant_x and constant_y:
        raise ValueError("A planned function does not make sense for two "
                         "constant inputs.")
    elif constant_x:
        use_case = base_case + 'b'
    elif constant_y:
        use_case = base_case + 'c'
    else:
        use_case = base_case + 'a'

    # ### Define function
    # 1-D correlation in 1-D or N-D sequences
    if base_case == '1':
        axes = axes[0]
        x_len = x_shape[axes]
        y_len = y_shape[axes]
        l = np.max((x_len, y_len))
        nfft = int(np.power(2, np.ceil(np.log2(2*l-1))))
        planned_rfft, planned_irfft = rfft(x_shape,
                                           nfft,
                                           axis=axes,
                                           fft_pair=True)

        rev_slices = [slice(None)] * x_ndim
        rev_slices[axes] = slice(None, None, -1)
        out_slices = [slice(None)] * x_ndim

        if mode == 'valid':
            if x_len < y_len:
                raise ValueError("x should have at least the same length as y "
                                 "for 'valid' mode")
            else:
                out_slices[axes] = slice(y_len - 1, x_len)

        elif mode == 'same':
            out_slices[axes] = slice((y_len - 1)//2, (y_len - 1)//2 + x_len)

        else:
            out_slices[axes] = slice(0, x_len + y_len - 1)

        if use_case == '1b':
            x_fft_0 = planned_rfft(plan_x)
            if correlate:
                def planned_convolve(y):
                    y_fft = planned_rfft(y[rev_slices])
                    return planned_irfft(x_fft_0 * y_fft)[out_slices]
            else:
                def planned_convolve(y):
                    y_fft = planned_rfft(y)
                    return planned_irfft(x_fft_0 * y_fft)[out_slices]

        elif use_case == '1c':
            if correlate:
                y_fft_0 = planned_rfft(plan_y[rev_slices])
            else:
                y_fft_0 = planned_rfft(plan_y)

            def planned_convolve(x):
                x_fft = planned_rfft(x)
                return planned_irfft(x_fft * y_fft_0)[out_slices]

        elif correlate:
            def planned_convolve(x, y):
                x_fft = planned_rfft(x)
                y_fft = planned_rfft(y[rev_slices])

                return planned_irfft(x_fft * y_fft)[out_slices]

        else:
            def planned_convolve(x, y):
                x_fft = planned_rfft(x)
                y_fft = planned_rfft(y)

                return planned_irfft(x_fft * y_fft)[out_slices]

    # M-D correlation in N-D sequences
    elif base_case == '2':
        # Define shapes and slices
        rev_slices = [slice(None, None, -1)] * y_ndim
        shape_max = np.max((x_shape, y_shape), axis=0)
        shape_max_p2 = np.power(2, np.ceil(np.log2(2*shape_max-1)))
        # noinspection PyUnresolvedReferences

        fft_shape = list(x_shape)
        for k in range(x_ndim):
            if k in axes:
                # noinspection PyUnresolvedReferences
                fft_shape[k] = shape_max_p2.astype(int)[k]

        # Plan rfftn and irfftn functions
        planned_rfftn, planned_irfftn = rfftn(tuple(shape_max),
                                              tuple(fft_shape),
                                              axes=axes,
                                              fft_pair=True)

        out_slices = [slice(None)] * x_ndim
        for k, x_n, y_n in zip(range(x_ndim), x_shape, y_shape):
            if mode == 'valid':
                if x_n < y_n:
                    raise ValueError("x should have at least the same "
                                     "length as y in all axes for 'valid' "
                                     "mode.")
                out_slices[k] = slice(y_n - 1, x_n)
            elif mode == 'same':
                out_slices[k] = slice((y_n - 1)//2, x_n + (y_n - 1)//2)
            else:
                out_slices[k] = slice(0, x_n + y_n - 1)

        if use_case == '2b':
            x_fft_0 = planned_rfftn(plan_x)

            if correlate:
                def planned_convolve(y):
                    y_fft = planned_rfftn(y[rev_slices])
                    return planned_irfftn(x_fft_0 * y_fft)[out_slices]
            else:
                def planned_convolve(y):
                    y_fft = planned_rfftn(y)
                    return planned_irfftn(x_fft_0 * y_fft)[out_slices]

        elif use_case == '2c':
            if correlate:
                y_fft_0 = planned_rfftn(plan_y[rev_slices])
            else:
                y_fft_0 = planned_rfftn(plan_y)

            def planned_convolve(x):
                x_fft = planned_rfftn(x)
                return planned_irfftn(x_fft * y_fft_0)[out_slices]

        elif correlate:
            def planned_convolve(x, y):
                x_fft = planned_rfftn(x)
                y_fft = planned_rfftn(y[rev_slices])
                r = planned_irfftn(x_fft * y_fft)[out_slices]
                return r
                # return planned_irfftn(x_fft * y_fft)[out_slices]

        else:
            def planned_convolve(x, y):
                x_fft = planned_rfftn(x)
                y_fft = planned_rfftn(y)
                r = planned_irfftn(x_fft * y_fft)[out_slices]
                return r

    # 1-D correlation of axis in N-D sequence with 1-D sequence
    elif base_case == '3':
        axes = axes[0]
        x_len = x_shape[axes]
        y_len = y_shape[0]
        l = np.max((x_len, y_len))
        nfft = int(np.power(2, np.ceil(np.log2(2*l-1))))
        planned_rfft, planned_irfft = rfft(x_shape,
                                           nfft,
                                           axis=axes,
                                           fft_pair=True)
        planned_rfft_2 = rfft(y_shape, nfft)

        out_slices = [slice(None)] * x_ndim

        if mode == 'valid':
            if x_len < y_len:
                raise ValueError("x should have at least the same length as y "
                                 "for 'valid' mode")
            else:
                out_slices[axes] = slice(y_len - 1, x_len)

        elif mode == 'same':
            out_slices[axes] = slice((y_len - 1)//2, (y_len - 1)//2 + x_len)

        else:
            out_slices[axes] = slice(0, x_len + y_len - 1)

        # If x is constant
        if use_case == '3b':
            x_fft_0 = planned_rfft(plan_x)

            if correlate:
                def planned_convolve(y):
                    y_fft = _utils.expand_me(planned_rfft_2(y[::-1]),
                                             axes,
                                             x_ndim)
                    return planned_irfft(x_fft_0 * y_fft)[out_slices]
            else:
                def planned_convolve(y):
                    y_fft = _utils.expand_me(planned_rfft_2(y), axes, x_ndim)
                    return planned_irfft(x_fft_0 * y_fft)[out_slices]

        # If y is constant
        elif use_case == '3c':
            if correlate:
                y_fft_0 = _utils.expand_me(np.fft.rfft(plan_y[::-1]),
                                           axes,
                                           x_ndim)
            else:
                y_fft_0 = _utils.expand_me(np.fft.rfft(plan_y), axes, x_ndim)

            def planned_convolve(x):
                x_fft = planned_rfft(x)
                return planned_irfft(x_fft * y_fft_0)[out_slices]

        # If neither x nor y are constant
        elif correlate:
            def planned_convolve(x, y):
                x_fft = planned_rfft(x)
                y_fft = _utils.expand_me(planned_rfft_2(y[::-1]), axes, x_ndim)
                return planned_irfft(x_fft * y_fft)[out_slices]

        else:
            def planned_convolve(x, y):
                x_fft = planned_rfft(x)
                y_fft = _utils.expand_me(planned_rfft_2(y), axes, x_ndim)
                return planned_irfft(x_fft * y_fft)[out_slices]

    # 1-D Correlation of 1-D sequence with axis in N-D sequence
    elif base_case == '4':
        axes = axes[0]
        x_len = x_shape[0]
        y_len = y_shape[axes]
        l = np.max((x_len, y_len))
        nfft = int(np.power(2, np.ceil(np.log2(2*l-1))))
        planned_rfft, planned_irfft = rfft(y_shape,
                                           nfft,
                                           axis=axes,
                                           fft_pair=True)
        planned_rfft_2 = rfft(x_shape, nfft)

        rev_slices = [slice(None)] * y_ndim
        rev_slices[axes] = slice(None, None, -1)
        out_slices = [slice(None)] * y_ndim

        if mode == 'valid':
            if x_len < y_len:
                raise ValueError("x should have at least the same length as y "
                                 "for 'valid' mode")
            else:
                out_slices[axes] = slice(y_len - 1, x_len)

        elif mode == 'same':
            out_slices[axes] = slice((y_len - 1)//2, (y_len - 1)//2 + x_len)

        else:
            out_slices[axes] = slice(0, x_len + y_len - 1)

        # If x is constant
        if use_case == '4b':
            x_fft_0 = _utils.expand_me(np.fft.rfft(plan_x, nfft), axes, y_ndim)

            if correlate:
                def planned_convolve(y):
                    y_fft = planned_rfft(y[rev_slices])
                    return planned_irfft(x_fft_0 * y_fft)[out_slices]
            else:
                def planned_convolve(y):
                    y_fft = planned_rfft(y)
                    return planned_irfft(x_fft_0 * y_fft)[out_slices]

        # If y is constant
        elif use_case == '4c':
            if correlate:
                y_fft_0 = np.fft.rfft(plan_y[rev_slices])
            else:
                y_fft_0 = np.fft.rfft(plan_y)

            def planned_convolve(x):
                x_fft = _utils.expand_me(planned_rfft_2(x), axes, y_ndim)
                return planned_irfft(x_fft * y_fft_0)[out_slices]

        # If neither x nor y are constant
        elif correlate:
            def planned_convolve(x, y):
                x_fft = _utils.expand_me(planned_rfft_2(x), axes, y_ndim)
                y_fft = planned_rfft(y[rev_slices])
                return planned_irfft(x_fft * y_fft)[out_slices]

        else:
            def planned_convolve(x, y):
                x_fft = _utils.expand_me(planned_rfft_2(x), axes, y_ndim)
                y_fft = planned_rfft(y)
                return planned_irfft(x_fft * y_fft)[out_slices]

    # X is segmented
    else:
        x_shape = x_shape[1:]
        x_ndim -= 1

        if base_case == '5a':
            axes = axes[0]
            if axes > 0:
                axes -= 1

            # Plan FFT
            x_len = x_shape[axes]
            y_len = y_shape[axes]
            l = np.max((x_len, y_len))
            nfft = int(np.power(2, np.ceil(np.log2(2*l-1))))
            planned_rfft, planned_irfft = rfft(x_shape,
                                               nfft,
                                               axis=axes,
                                               fft_pair=True)

            # Define slices
            rev_slices = [slice(None)] * x_ndim
            rev_slices[axes] = slice(None, None, -1)
            out_slices = [slice(None)] * x_ndim

            if mode == 'valid':
                if x_len < y_len:
                    raise ValueError("x should have at least the same length "
                                     "as y for 'valid' mode")
                else:
                    out_slices[axes] = slice(y_len - 1, x_len)

            elif mode == 'same':
                out_slices[axes] = slice((y_len - 1)//2, (y_len - 1)//2 + x_len)

            else:
                out_slices[axes] = slice(0, x_len + y_len - 1)

            # Pre-compute FFT for all segments of x
            x_fft_0 = []
            for segment in plan_x:
                x_fft_0.append(planned_rfft(segment))

            if correlate:
                def planned_convolve(n, y):
                    y_fft = planned_rfft(y[rev_slices])
                    return planned_irfft(x_fft_0[n] * y_fft)[out_slices]
            else:
                def planned_convolve(n, y):
                    y_fft = planned_rfft(y)
                    return planned_irfft(x_fft_0[n] * y_fft)[out_slices]

        elif base_case == '5b':
            axes = [axis - 1 if axis > 0 else axis for axis in axes]

            # Compute shapes
            shape_max = np.max((x_shape, y_shape), axis=0)
            shape_max_p2 = np.power(2, np.ceil(np.log2(2*shape_max-1)))

            fft_shape = list(x_shape)
            for k in range(x_ndim):
                if k in axes:
                    # noinspection PyUnresolvedReferences
                    fft_shape[k] = shape_max_p2.astype(int)[k]

            # Plan rfftn and irfftn functions
            planned_rfftn, planned_irfftn = rfftn(tuple(shape_max),
                                                  tuple(fft_shape),
                                                  axes=axes,
                                                  fft_pair=True)

            # Define slices
            rev_slices = [slice(None, None, -1)] * y_ndim
            out_slices = [slice(None)] * x_ndim
            for k, x_n, y_n in zip(range(x_ndim), x_shape, y_shape):
                if mode == 'valid':
                    if x_n < y_n:
                        raise ValueError("x should have at least the same "
                                         "length as y in all axes for 'valid' "
                                         "mode.")
                    out_slices[k] = slice(y_n - 1, x_n)
                elif mode == 'same':
                    out_slices[k] = slice((y_n - 1)//2, x_n + (y_n - 1)//2)
                else:
                    out_slices[k] = slice(0, x_n + y_n - 1)

            x_fft_0 = []
            for segment in plan_x:
                x_fft_0.append(planned_rfftn(segment))

            if correlate:
                def planned_convolve(n, y):
                    y_fft = planned_rfftn(y[rev_slices])
                    return planned_irfftn(x_fft_0[n] * y_fft)[out_slices]
            else:
                def planned_convolve(n, y):
                    y_fft = planned_rfftn(y)
                    return planned_irfftn(x_fft_0[n] * y_fft)[out_slices]

        # Convolve/correlate single axis in N-d segment with 1-d sequence
        else:
            axes = axes[0]
            if axes > 0:
                axes -= 1
            print(x_shape)
            print(axes)
            print(y_shape)
            x_len = x_shape[axes]
            y_len = y_shape[0]
            l = np.max((x_len, y_len))
            nfft = int(np.power(2, np.ceil(np.log2(2*l-1))))
            planned_rfft, planned_irfft = rfft(x_shape,
                                               nfft,
                                               axis=axes,
                                               fft_pair=True)
            planned_rfft_2 = rfft(y_shape, nfft)

            out_slices = [slice(None)] * x_ndim

            if mode == 'valid':
                if x_len < y_len:
                    raise ValueError("x should have at least the same length "
                                     "as y for 'valid' mode")
                else:
                    out_slices[axes] = slice(y_len - 1, x_len)

            elif mode == 'same':
                out_slices[axes] = slice((y_len - 1)//2, (y_len - 1)//2 + x_len)

            else:
                out_slices[axes] = slice(0, x_len + y_len - 1)

            x_fft_0 = []
            for segment in plan_x:
                x_fft_0.append(planned_rfft(segment))

            if correlate:
                def planned_convolve(n, y):
                    y_fft = _utils.expand_me(planned_rfft_2(y[::-1]),
                                             axes,
                                             x_ndim)
                    return planned_irfft(x_fft_0[n] * y_fft)[out_slices]
            else:
                def planned_convolve(n, y):
                    y_fft = _utils.expand_me(planned_rfft_2(y), axes, x_ndim)
                    return planned_irfft(x_fft_0[n] * y_fft)[out_slices]

    return planned_convolve


# ### Public functions
def firfilter(plan_b,
              plan_x,
              axis=-1,
              nfft=None,
              constant_signal=False,
              constant_filter=False,
              x_segmented=False,
              segments_axis=0):
    """Returns a planned function that filters a signal using the frequency
    domain overlap-and-add method with pyfftw.

    Parameters
    ----------
        plan_b : integer, shape or array-like
            A filter vector or its length or shape.
        plan_x : integer, shape or array-like
            A signal vector or its length or shape.
        axis : optional[int]
            Axis in plan_x along which the filter is applied.
        nfft : optional[int]
            FFT size. Default is selected for fastest computation based on
            signal and filter shapes.
        constant_signal : optional[boolean]
            Set to True if the signal is constant over all function calls and
            only the filter will change. Default is False.
        constant_filter : optional[boolean]
            Set to True if the filter is constant over all function calls and
            only the signal will change. Default is False.
        x_segmented : optional[boolean]
            Set to True if the signal is divided into segments along some axis
            and each segment is filtered on it's own multiple times. Default
            is False.
        segments_axis : optional[boolean]
            Axis along which segments are located. Default is 0.

    Returns
    -------
        function
            A planned FIR-filtering function.

    Raises
    ------
        ValueError
            If filter has more than one dimensions.
            If signal and filter are both constant.
            If signal is constant but not array-like.
            If filter is constant but not array-like.
            If signal is segmented but not constant.
    """

    # Get dimensions
    b_shape = _utils.get_shape(plan_b)
    x_shape = _utils.get_shape(plan_x)
    b_ndim = len(b_shape)
    x_ndim = len(x_shape)
    n_filter = b_shape[-1]
    n_signal = x_shape[axis]
    n_of_segments = x_shape[segments_axis]

    # ### Validate input
    # Check that plan_b has no more than one dimension
    if b_ndim > 2:
        raise ValueError("plan_b cannot have more than one dimension")
    elif b_ndim == 2 and not b_shape[0] == 1:
            raise ValueError("plan_b cannot have more than one dimension")

    # Having both a constant signal and a constant filter makes no sense
    if constant_signal and constant_filter:
        raise ValueError("signal and filter cannot both be constant.")

    # If signal is constant, plan_x must be actual data
    if constant_signal:
        # Make sure plan_x is a numpy array
        if not isinstance(plan_x, np.ndarray):
            try:
                plan_x = np.array(plan_x, dtype='float64')
            except ValueError:
                raise ValueError("plan_x must be array-like if constant_signal "
                                 "is True")

    # If filter is constant, plan_b must be an actual filter vector
    if constant_filter:
        # Make sure plan_b is a numpy array
        if not isinstance(plan_b, np.ndarray):
            try:
                plan_b = np.array(plan_b, dtype='float64')
            except ValueError:
                raise ValueError("plan_b must be array-like if constant_filter "
                                 "is True")

    # If plan_x is segmented, make sure plan_x has at least two dimensions
    if x_segmented:
        constant_signal = True
        if x_ndim < 2:
            raise ValueError("A segmented signal must have at least two "
                             "dimensions")

    # ### Find use_case
    if x_segmented:
        if x_ndim > 2:
            use_case = '3b'
        else:
            use_case = '3a'
    elif x_ndim > 1:
        if constant_filter:
            use_case = '2c'
        elif constant_signal:
            use_case = '2b'
        else:
            use_case = '2a'
    else:
        if constant_filter:
            use_case = '1c'
        elif constant_signal:
            use_case = '1b'
        else:
            use_case = '1a'

    # ### Compute nfft if not explicitly given
    try:
        nfft = int(nfft)
    except TypeError:
        nfft = _utils.compute_nfft(n_filter, n_signal)

    # ### nfft_complex = nfft//2 + 1

    # ### Make pyfftw plans
    # define shapes
    u_shape = list(x_shape)
    y_shape = list(x_shape)
    u_shape[axis] = nfft

    # Reduce by one dimension if plan_x contains segments
    if x_segmented:
        u_shape.pop(segments_axis)
        y_shape.pop(segments_axis)
        axis = _utils.get_segment_axis(x_shape, axis, segments_axis)

    # Create the arrays and objects

    planned_rfft, planned_irfft = rfft(tuple(u_shape),
                                       nfft,
                                       axis=axis,
                                       fft_pair=True)

    # ### Common preparations for multiple cases
    l = nfft - n_filter + 1

    t = list(range(len(u_shape)))
    t[axis], t[-1] = t[-1], t[axis]

    filter_expander = np.ones(u_shape).transpose(t)

    if use_case == '3b':
        slices = [slice(None)] * (x_ndim - 1)
    else:
        slices = [slice(None)] * x_ndim

    # ### Case 1a: 1-d signal
    if use_case == '1a':
        def planned_firfilter(b, x):
            """Filter data with a FIR filter.

            Parameters
            ----------
                b : array-like
                    A one-dimensional FIR filter array
                x : array-like
                    A one-dimensional input array

            Returns
            -------
                numpy.array
                    Filter output
            """
            # nfft-point FFT of filter once
            b_fft = planned_rfft(np.hstack((b, np.zeros(nfft - n_filter))))

            y = np.zeros(y_shape)
            for k in range(0, n_signal, l):
                k_to = np.min((k + l, n_signal))
                x_fft = planned_rfft(np.hstack((x[k:k_to],
                                                np.zeros(nfft - (k_to - k)))))
                y_fft = planned_irfft(x_fft * b_fft)
                y_to = np.min((n_signal, k + nfft))
                y[k:y_to] = y[k:y_to] + y_fft[:y_to - k].real

            return y

    # ### Case 1b: 1-d signal, constant signal
    elif use_case == '1b':
        # Pre-compute partial FFTs of x
        x_fft_list = []
        for k_0 in range(0, n_signal, l):
            k_0_to = np.min((k_0 + l, n_signal))
            x_fft_list.append(planned_rfft(
                np.hstack((plan_x[k_0:k_0_to],
                           np.zeros(nfft - (k_0_to - k_0))))))

        def planned_firfilter(b):
            """Filter constant data with a FIR filter.

            Parameters
            ----------
                b : array-like
                    A one-dimensional FIR filter array.

            Returns
            -------
                numpy.array
                    Filter output
            """
            # nfft-point FFT of filter once
            b_fft = planned_rfft(np.hstack((b, np.zeros(nfft - n_filter))))

            y = np.zeros(y_shape)
            list_idx = 0
            for k in range(0, n_signal, l):
                y_fft = planned_irfft(x_fft_list[list_idx] * b_fft)
                y_to = np.min((n_signal, k + nfft))
                y[k:y_to] = y[k:y_to] + y_fft[:y_to - k].real
                list_idx += 1

            return y

    # ### Case 1c: 1-d signal, constant filter
    elif use_case == '1c':
        bb_fft = planned_rfft(np.hstack((plan_b, np.zeros(nfft - n_filter))))

        def planned_firfilter(x):
            """Filter data with a constant FIR filter.

            Parameters
            ----------
                x : array-like
                    A one-dimensional input array

            Returns
            -------
                numpy.array
                    Filter output
            """
            y = np.zeros(y_shape)
            for k in range(0, n_signal, l):
                k_to = np.min((k + l, n_signal))
                x_fft = planned_rfft(np.hstack((x[k:k_to],
                                                np.zeros(nfft - (k_to - k)))))
                y_fft = planned_irfft(x_fft * bb_fft)
                y_to = np.min((n_signal, k + nfft))
                y[k:y_to] = y[k:y_to] + y_fft[:y_to - k].real

            return y

    # ### Case 2a: N-d signal
    elif use_case == '2a':
        def planned_firfilter(b, x):
            """Filter data with a FIR filter.

            Parameters
            ----------
                b : array-like
                    A one-dimensional FIR filter array
                x : array-like
                    An N-dimensional input array

            Returns
            -------
                numpy.array
                    Filter output
            """
            # nfft-point FFT of filter once
            b_padded = np.hstack((b, np.zeros(nfft - n_filter)))
            b_fft = planned_rfft((b_padded*filter_expander).transpose(t))

            y = np.zeros(y_shape)
            for k in range(0, n_signal, l):
                k_to = np.min((k + l, n_signal))
                slices[axis] = slice(k, k_to)
                x_fft = planned_rfft(_utils.pad_array(x[slices], u_shape))
                y_to = np.min((n_signal, k + nfft))
                # noinspection PyTypeChecker
                slices[axis] = slice(None, y_to - k)
                y_fft = planned_irfft(x_fft * b_fft)[slices]
                slices[axis] = slice(k, y_to)
                y[slices] = y[slices] + y_fft.real

            return y

    # ### Case 2b: N-d signal, constant signal
    elif use_case == '2b':
        # Pre-compute partial FFTs of x
        x_fft_list = []
        for k_0 in range(0, n_signal, l):
            k_0_to = np.min((k_0 + l, n_signal))
            slices[axis] = slice(k_0, k_0_to)
            x_fft_list.append(planned_rfft(_utils.pad_array(plan_x[slices],
                                                            u_shape)))

        def planned_firfilter(b):
            """Filter static data with a FIR filter.

            Parameters
            ----------
                b : array-like
                    A one-dimensional FIR filter array.

            Returns
            -------
                numpy.array
                    Filter output
            """
            # nfft-point FFT of filter once
            b_padded = np.hstack((b, np.zeros(nfft - n_filter)))
            b_fft = planned_rfft((b_padded*filter_expander).transpose(t))

            y = np.zeros(y_shape)
            list_idx = 0
            for k in range(0, n_signal, l):
                y_to = np.min((n_signal, k + nfft))
                # noinspection PyTypeChecker
                slices[axis] = slice(None, y_to - k)
                y_fft = planned_irfft(x_fft_list[list_idx] * b_fft)[slices]
                slices[axis] = slice(k, y_to)
                y[slices] = y[slices] + y_fft.real
                list_idx += 1

            return y

    # ### Case 2c: N-d signal, constant filter
    elif use_case == '2c':
        bb_padded = np.hstack((plan_b, np.zeros(nfft - n_filter)))
        bb_fft = planned_rfft((bb_padded*filter_expander).transpose(t))

        def planned_firfilter(x):
            """Filter data with a constant FIR filter.

            Parameters
            ----------
                b : array-like
                    A one-dimensional FIR filter array
                x : array-like
                    An N-dimensional input array

            Returns
            -------
                numpy.array
                    Filter output
            """
            y = np.zeros(y_shape)
            for k in range(0, n_signal, l):
                k_to = np.min((k + l, n_signal))
                slices[axis] = slice(k, k_to)
                x_fft = planned_rfft(_utils.pad_array(x[slices], u_shape))
                y_to = np.min((n_signal, k + nfft))
                # noinspection PyTypeChecker
                slices[axis] = slice(None, y_to - k)
                y_fft = planned_irfft(x_fft * bb_fft)[slices]
                slices[axis] = slice(k, y_to)
                y[slices] = y[slices] + y_fft.real

            return y

    # ### Case 3a: 1-d signal segments, constant signal
    elif use_case == '3a':
        # Pre-compute partial FFTs of x segments
        x_fft_list = []
        segment_slices = [slice(None)] * x_ndim
        for k_s in range(n_of_segments):
            segment_slices[segments_axis] = slice(k_s, k_s + 1)
            x_segment = np.squeeze(plan_x[segment_slices])
            this_x_fft_list = []
            for k_p in range(0, n_signal, l):
                k_p_to = np.min((k_p + l, n_signal))
                this_x_fft_list.append(planned_rfft(
                    _utils.pad_array(x_segment[k_p:k_p_to], u_shape)))
            x_fft_list.append(this_x_fft_list)

        def planned_firfilter(b, segment_no):
            """Filter constant data with a FIR filter.

            Parameters
            ----------
                b : array-like
                    A one-dimensional FIR filter array.
                segment_no : int
                    Segment number

            Returns
            -------
                numpy.array
                    Filter output
            """
            # nfft-point FFT of filter once
            b_fft = planned_rfft(np.hstack((b, np.zeros(nfft - n_filter))))

            y = np.zeros(y_shape)
            list_idx = 0
            for k in range(0, n_signal, l):
                y_fft = planned_irfft(x_fft_list[segment_no][list_idx] * b_fft)
                y_to = np.min((n_signal, k + nfft))
                y[k:y_to] = y[k:y_to] + y_fft[:y_to - k].real
                list_idx += 1

            return y

    # ### Case 3b: 2-d signal segments, constant signal
    else:
        # Pre-compute partial FFTs of x segments
        segment_slices = [slice(None)] * x_ndim
        x_fft_list = []
        for k_s in range(n_of_segments):
            segment_slices[segments_axis] = slice(k_s, k_s + 1)
            x_segment = np.squeeze(plan_x[segment_slices])
            this_x_fft_list = []
            for k_p in range(0, n_signal, l):
                k_p_to = np.min((k_p + l, n_signal))
                slices[axis] = slice(k_p, k_p_to)
                this_x_fft_list.append(planned_rfft(
                    _utils.pad_array(x_segment[slices], u_shape)))
            x_fft_list.append(this_x_fft_list)

        def planned_firfilter(b, segment_no):
            """Filter static data with a FIR filter.

            Parameters
            ----------
                b : array-like
                    A one-dimensional FIR filter array.
                segment_no : int
                    Index of the segment to filter.

            Returns
            -------
                numpy.array
                    Filter output
            """
            # nfft-point FFT of filter once
            b_padded = np.hstack((b, np.zeros(nfft - n_filter)))
            b_fft = planned_rfft((b_padded*filter_expander).transpose(t))

            y = np.zeros(y_shape)
            list_idx = 0
            for k in range(0, n_signal, l):
                y_to = np.min((n_signal, k + nfft))
                # noinspection PyTypeChecker
                slices[axis] = slice(None, y_to - k)
                y_fft = planned_irfft(
                    x_fft_list[segment_no][list_idx] * b_fft)[slices]
                slices[axis] = slice(k, y_to)
                y[slices] = y[slices] + y_fft.real
                list_idx += 1

            return y

    return planned_firfilter


def convolve(plan_x,
             plan_y,
             mode='full',
             axes=None,
             constant_x=False,
             constant_y=False,
             x_segmented=False):
    """Returns a planned function for computing the convolution of two
    sequences or arrays.

    The planner distinguishes between several different use cases:

        1. 1-D convolution of 1-D sequences or along single axis in N-D arrays
        2. M-D convolution of N-D sequences
        3. 1-D convolution along single axis in N-D array with 1-D sequence
        4. 1-D convolution of 1-D sequence along single axis in N-D array
        5. Special cases of 1, 2 and 3 where the first input is segmented

        The shapes of the two inputs are usually sufficient to determine which
        case should be used. However, to get 1-D convolution along single axis
        in N-D arrays, 'axes' must be a single integer or a length 1 sequence.
        In addition, x_segmented must be True for case 5.

    Parameters
    ----------
        plan_x : integer, shape or array-like
            First input sequence, it's shape or length.
        plan_y : integer, shape or array-like
            Second input sequence, it's shape or length.
        mode : Optional[str]
            A string indicating the output size.

            'full'
                The output is the full discrete linear convolution of the
                inputs. (Default)
            'valid'
                The output consists only of those elements that do not rely on
                zero-padding.
            'same'
                The output is the same size as plan_x, centered with respect to
                the 'full' output.
        axes : Optional[int or sequence of ints]
            The axis or axes along which the convolution is computed.
            Default is the last N axes of the highest-rank input where N is the
            rank of the lowest-rank input.
        constant_x : Optional[boolean]
            Indicates that the first input will be constant over all uses of
            the function. If True, plan_x must be array-like.
        constant_y : Optional[boolean]
            Indicates that the second input will be constant over all uses of
            the function. If True, plan_y must be array-like.
        x_segmented : Optional[boolean]
            Indicates that the first axis of plan_x contains segments that will
            be individually used multiple times.

    Returns
    -------
        function
            Planned convolution function.

    Raises
    ------
        ValueError
            If no function can be planned for the given arguments.
    """

    return _convolve(plan_x,
                     plan_y,
                     False,
                     mode,
                     axes,
                     constant_x,
                     constant_y,
                     x_segmented)


def correlate(plan_x,
              plan_y,
              mode='full',
              axes=None,
              constant_x=False,
              constant_y=False,
              x_segmented=False):
    """Returns a planned function for computing the cross-correlation of two
    sequences or arrays.

    The planner distinguishes between several different use cases:

        1. 1-D correlation of 1-D sequences or along single axis in N-D arrays
        2. M-D correlation of N-D sequences
        3. 1-D correlation along single axis in N-D array with 1-D sequence
        4. 1-D correlation of 1-D sequence along single axis in N-D array
        5. Special cases of 1, 2 and 3 where the first input is segmented

        The shapes of the two inputs are usually sufficient to determine which
        case should be used. However, to get 1-D correlation along single axis
        in N-D arrays, 'axes' must be a single integer or a length 1 sequence.
        In addition, x_segmented must be True for case 5.

    Parameters
    ----------
        plan_x : integer, shape or array-like
            First input sequence, it's shape or length.
        plan_y : integer, shape or array-like
            Second input sequence, it's shape or length.
        mode : Optional[str]
            A string indicating the output size.

            'full'
                The output is the full discrete linear cross-correlation of the
                inputs. (Default)
            'valid'
                The output consists only of those elements that do not rely on
                zero-padding.
            'same'
                The output is the same size as plan_x, centered with respect to
                the 'full' output.
        axes : Optional[int or sequence of ints]
            The axis or axes along which the cross-correlation is computed.
            Default is the last N axes of the highest-rank input where N is the
            rank of the lowest-rank input.
        constant_x : Optional[boolean]
            Indicates that the first input will be constant over all uses of
            the function. If True, plan_x must be array-like.
        constant_y : Optional[boolean]
            Indicates that the second input will be constant over all uses of
            the function. If True, plan_y must be array-like.
        x_segmented : Optional[boolean]
            Indicates that the first axis of plan_x contains segments that will
            be individually used multiple times.

    Returns
    -------
        function
            Planned correlation function.

    Raises
    ------
        ValueError
            If no function can be planned for the given arguments.
    """

    return _convolve(plan_x,
                     plan_y,
                     True,
                     mode,
                     axes,
                     constant_x,
                     constant_y,
                     x_segmented)
