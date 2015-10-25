#!usr/bin/env python

import pyfftw
import numpy as np
try:
    from . import _utils
except ImportError:
    import _utils


def fft(a, nfft=None, axis=-1, fft_pair=False, crop_ifft=False):
    """Returns a planned function that computes the 1-D DFT of a sequence
    or array.

    Parameters
    ----------
        a : number, shape or array-like
            An input array, its shape or length.
        nfft : Optional[int]
            Number of FFT points. Default is input size along specified
            axis
        axis : Optional[int]
            Axis along which to perform the fft. Default is -1.
        fft_pair : Optional[boolean]
            Indicates Whether or not to also return an ifft function.
            Default is False.
        crop_ifft : Optional[boolean]
            Indicates whether the planned ifft function should crop its
            output to match input size. Default is False.

    Returns
    -------
        planned_fft(x)
            Planned fft function.
        planned_ifft(x)
            Planned ifft function. Returned if fft_pair is True.
    """
    # Get shape
    shape = _utils.get_shape(a)
    n = shape[axis]

    # Set up slices and pyfftw shapes
    n_dim = len(shape)
    slices = [slice(None)] * n_dim

    if nfft is None:
        nfft = shape[axis]
    else:
        shape = list(shape)
        shape[axis] = nfft

    # Set data type
    if np.asarray(a).dtype.name in ('float32', 'int32'):
        dtype = 'complex64'
    else:
        dtype = 'complex128'

    # Set up input and output arrays and FFT object
    u = pyfftw.n_byte_align_empty(shape, 16, dtype)
    v = pyfftw.n_byte_align_empty(shape, 16, dtype)
    fft_obj = pyfftw.FFTW(u, v, direction='FFTW_FORWARD', axes=(axis,))

    # Define fft function
    if n == nfft:
        def planned_fft(x):
            u[:] = x
            return fft_obj().copy()

    elif n < nfft:
        def planned_fft(x):
            u[:] = _utils.pad_array(x, shape)
            return fft_obj().copy()

    else:
        slices[axis] = slice(0, nfft)

        def planned_fft(x):
            u[:] = x[slices]
            return fft_obj().copy()

    # Define ifft function
    if fft_pair is True:
        ifft_obj = pyfftw.FFTW(v, u, direction='FFTW_BACKWARD',
                               axes=(axis,))

        if n > nfft:
            raise ValueError("NFFT must be at least equal to signal "
                             "length when returning an FFT pair.")

        elif n < nfft and crop_ifft:
            slices[axis] = slice(None, n)

            def planned_ifft(x):
                v[:] = x
                return ifft_obj().copy()[slices]

        else:
            def planned_ifft(x):
                v[:] = x
                return ifft_obj().copy()

        return planned_fft, planned_ifft

    else:
        return planned_fft


def rfft(a, nfft=None, axis=-1, fft_pair=False, crop_ifft=False):
    """Returns a planned function that computes the 1-D DFT of a real-valued
    sequence or array.

    Parameters
    ----------
        a : number, shape or array-like
            An input array, its shape or length.
        nfft : Optional[int]
            Number of FFT points. Default is input size along specified axis
        axis : Optional[int]
            Axis along which to perform the fft. Default is -1.
        fft_pair : Optional[boolean]
            Indicates Whether or not to also return an ifft function.
            Default is False.
        crop_ifft : Optional[boolean]
            Indicates whether the planned ifft function should crop its
            output to match input size. Default is False.

    Returns
    -------
        planned_rfft(x)
            Planned fft function.
        planned_irfft(x)
            Planned ifft function. Returned if fft_pair is True.
    """
    # Get shape
    a_shape = _utils.get_shape(a)
    n = a_shape[axis]

    # Set up slices and pyfftw shapes
    n_dim = len(a_shape)
    slices = [slice(None)] * n_dim

    if nfft is None:
        nfft = a_shape[axis]

    u_shape = list(a_shape)
    v_shape = list(a_shape)
    u_shape[axis] = nfft
    v_shape[axis] = nfft//2 + 1

    # Set data types
    if np.asarray(a).dtype.name == 'float32':
        dtype = 'float32'
        fft_dtype = 'complex64'
    else:
        dtype = 'float64'
        fft_dtype = 'complex128'

    u = pyfftw.n_byte_align_empty(u_shape, 16, dtype)
    v = pyfftw.n_byte_align_empty(v_shape, 16, fft_dtype)
    fft_obj = pyfftw.FFTW(u, v, direction='FFTW_FORWARD', axes=(axis,))

    # Define fft function
    if n == nfft:
        def planned_rfft(x):
            u[:] = x
            return fft_obj().copy()

    elif n < nfft:
        def planned_rfft(x):
            u[:] = _utils.pad_array(x, u_shape)
            return fft_obj().copy()

    else:
        slices[axis] = slice(0, nfft)

        def planned_rfft(x):
            u[:] = x[slices]
            return fft_obj().copy()

    # Define ifft function
    if fft_pair is True:
        ifft_obj = pyfftw.FFTW(v, u, direction='FFTW_BACKWARD',
                               axes=(axis,))

        if n > nfft:
            raise ValueError("NFFT must be at least equal to signal "
                             "length when returning an FFT pair.")

        elif n < nfft and crop_ifft:
            slices[axis] = slice(None, n)

            def planned_irfft(x):
                v[:] = x
                return ifft_obj().copy()[slices]

        else:
            def planned_irfft(x):
                v[:] = x
                return ifft_obj().copy()

        return planned_rfft, planned_irfft

    else:
        return planned_rfft


def fftn(a, shape=None, axes=None, fft_pair=False, crop_ifft=False):
    """Returns a planned function that computes the N-D DFT of an array.

    Parameters
    ----------
        a : array-like or shape
            An input array or its shape
        nfft : Optional[sequence of ints]
            Number of FFT points. Default is input size along specified axes
        axes : Optional[sequence of ints]
            Axes along which to perform the fft. Default is all axes.
        fft_pair : Optional[boolean]
            Indicates Whether or not to also return an ifft function. Default
            is False.
        crop_ifft : Optional[boolean]
            Indicates whether the planned ifft function should crop its output
            to match input size. Default is False.

    Returns
    -------
        planned_fftn(x)
            Planned fft function.
        planned_ifftn(x)
            Planned ifft function. Returned if fft_pair is True.
    """
    # Get shape of input
    a_shape = _utils.get_shape(a)
    n_dim = len(a_shape)

    if shape is None:
        if axes is None:
            shape = a_shape
        else:
            shape = [a_shape[axis] for axis in axes]

    if axes is None:
        n_dim_s = len(shape)
        dim_diff = n_dim - n_dim_s
        axes = [k + dim_diff for k in range(n_dim_s)]

    # Make sure axes and shape are iterable
    if np.asarray(axes).ndim == 0:
        axes = (axes,)
    if np.asarray(shape).ndim == 0:
        shape = (shape,)

    # Compute FFTW shape
    fft_shape = list(a_shape)
    for n, axis in zip(range(len(axes)), axes):
        fft_shape[axis] = shape[n]

    # Set up slices
    slices = [slice(None)] * n_dim
    for axis in axes:
        slices[axis] = slice(0, fft_shape[axis])

    # Set data type
    if np.asarray(a).dtype.name in ('float32', 'int32'):
        dtype = 'complex64'
    else:
        dtype = 'complex128'

    u = pyfftw.n_byte_align_empty(fft_shape, 16, dtype)
    v = pyfftw.n_byte_align_empty(fft_shape, 16, dtype)
    fft_obj = pyfftw.FFTW(u, v, direction="FFTW_FORWARD", axes=axes)

    has_smaller_axis = any(s1 < s2 for s1, s2 in zip(a_shape, fft_shape))
    has_larger_axis = any(s1 > s2 for s1, s2 in zip(a_shape, fft_shape))

    # Define fft function
    if has_smaller_axis and has_larger_axis:
        def planned_fftn(x):
            u[:] = _utils.pad_array(x[slices], fft_shape)
            return fft_obj().copy()

    elif has_larger_axis:
        def planned_fftn(x):
            u[:] = x[slices]
            return fft_obj().copy()

    elif has_smaller_axis:
        def planned_fftn(x):
            u[:] = _utils.pad_array(x, fft_shape)
            return fft_obj().copy()

    else:
        def planned_fftn(x):
            u[:] = x
            return fft_obj().copy()

    # Define ifftn function
    if fft_pair is True:
        ifft_obj = pyfftw.FFTW(v, u, direction='FFTW_BACKWARD', axes=axes)

        if has_larger_axis:
            raise ValueError("Number of FFT points must be equal to or greater"
                             "than the signal length for each axis when "
                             "returning an FFT pair")

        elif has_smaller_axis and crop_ifft:
            for axis in axes:
                slices[axis] = slice(0, a_shape[axis])

            def planned_ifftn(x):
                v[:] = x
                return ifft_obj().copy()[slices]
        else:
            def planned_ifftn(x):
                v[:] = x
                return ifft_obj().copy()

        return planned_fftn, planned_ifftn

    else:
        return planned_fftn


def rfftn(a, shape=None, axes=None, fft_pair=False, crop_ifft=False):
    """Returns a planned function that computes the N-D DFT of a real-valued
    array.

    Parameters
    ----------
        a : array-like or shape
            An input array or its shape.
        nfft : Optional[sequence of ints]
            Number of FFT points. Default is input size along specified axes
        axes : Optional[sequence of ints]
            Axes along which to perform the fft. Default is all axes.
        fft_pair : Optional[boolean]
            Indicates Whether or not to also return an ifft function. Default
            is False.
        crop_ifft : Optional[boolean]
            Indicates whether the planned ifft function should crop its output
            to match input size. Default is False.

    Returns
    -------
        planned_rfftn(x)
            Planned fft function.
        planned_irfftn(x)
            Planned ifft function. Returned if fft_pair is True.
    """
    # Get shape of input
    a_shape = _utils.get_shape(a)
    n_dim = len(a_shape)

    if shape is None:
        if axes is None:
            shape = a_shape
        else:
            shape = [a_shape[axis] for axis in axes]

    if axes is None:
        n_dim_s = len(shape)
        dim_diff = n_dim - n_dim_s
        axes = [k + dim_diff for k in range(n_dim_s)]

    # Make sure axes and shape are iterable
    if np.asarray(axes).ndim == 0:
        axes = (axes,)
    if np.asarray(shape).ndim == 0:
        shape = (shape,)

    # Compute FFTW shape
    u_shape = list(a_shape)
    v_shape = list(a_shape)

    for n, axis in zip(range(len(axes)), axes):
        u_shape[axis] = shape[n]
        v_shape[axis] = shape[n]

    v_shape[axes[-1]] = v_shape[axes[-1]]//2 + 1

    # Set up slices
    slices = [slice(None)] * n_dim
    for axis in axes:
        slices[axis] = slice(0, u_shape[axis])

    # Set data type
    if np.asarray(a).dtype.name in ('float32', 'int32'):
        dtype = 'float32'
        fft_dtype = 'complex64'
    else:
        dtype = 'float64'
        fft_dtype = 'complex128'

    u = pyfftw.n_byte_align_empty(u_shape, 16, dtype)
    v = pyfftw.n_byte_align_empty(v_shape, 16, fft_dtype)

    fft_obj = pyfftw.FFTW(u, v, direction="FFTW_FORWARD", axes=axes)

    has_smaller_axis = any(s1 < s2 for s1, s2 in zip(a_shape, u_shape))
    has_larger_axis = any(s1 > s2 for s1, s2 in zip(a_shape, u_shape))

    # Define fft function
    if has_smaller_axis and has_larger_axis:
        def planned_rfftn(x):
            u[:] = _utils.pad_array(x[slices], u_shape)
            return fft_obj().copy()

    elif has_larger_axis:
        def planned_rfftn(x):
            u[:] = x[slices]
            return fft_obj().copy()

    elif has_smaller_axis:
        def planned_rfftn(x):
            u[:] = _utils.pad_array(x, u_shape)
            return fft_obj().copy()

    else:
        def planned_rfftn(x):
            u[:] = x
            return fft_obj().copy()

    # Define ifftn function
    if fft_pair is True:
        ifft_obj = pyfftw.FFTW(v, u, direction='FFTW_BACKWARD', axes=axes)

        if has_larger_axis:
            raise ValueError("Number of FFT points must be equal to or greater"
                             "than the signal length for each axis when "
                             "returning an FFT pair")

        elif has_smaller_axis and crop_ifft:
            for axis in axes:
                slices[axis] = slice(0, a_shape[axis])

            def planned_irfftn(x):
                v[:] = x
                return ifft_obj().copy()[slices]
        else:
            def planned_irfftn(x):
                v[:] = x
                return ifft_obj().copy()

        return planned_rfftn, planned_irfftn

    else:
        return planned_rfftn


def ifft(a, nfft=None, axis=-1, fft_pair=False, crop_fft=False):
    """Returns a planned function that computes the 1-D inverse DFT of a
    sequence or array.

    Parameters
    ----------
        a : number, shape or array-like
            An input array, its shape or length.
        nfft : Optional[int]
            Number of FFT points. Default is input size along specified axis
        axis : Optional[int]
            Axis along which to perform the fft. Default is -1.
        fft_pair : Optional[boolean]
            Indicates Whether or not to also return an ifft function. Default
            is False.
        crop_fft : Optional[boolean]
            Indicates that the fft function should crop its output to match
            the shape of the input to the ifft function

    Returns
    -------
        planned_ifft(x)
            Planned ifft function.
        planned_fft(x)
            Planned fft function. Returned if fft_pair is True.
    """
    # Get shape
    shape = _utils.get_shape(a)
    n = shape[axis]

    # Set up slices and pyfftw shapes
    n_dim = len(shape)
    slices = [slice(None)] * n_dim

    if nfft is None:
        nfft = shape[axis]
    else:
        shape = list(shape)
        shape[axis] = nfft

    # Set data type
    if np.asarray(a).dtype.name in ('float32', 'int32', 'complex64'):
        dtype = 'complex64'
    else:
        dtype = 'complex128'

    # Set up input and output arrays and FFT object
    u = pyfftw.n_byte_align_empty(shape, 16, dtype)
    v = pyfftw.n_byte_align_empty(shape, 16, dtype)
    ifft_obj = pyfftw.FFTW(v, u, direction='FFTW_BACKWARD', axes=(axis,))

    # Define fft function
    if n == nfft:
        def planned_ifft(x):
            v[:] = x
            return ifft_obj().copy()

    elif n < nfft:
        def planned_ifft(x):
            v[:] = _utils.pad_array(x, shape)
            return ifft_obj().copy()

    else:
        slices[axis] = slice(0, nfft)

        def planned_ifft(x):
            v[:] = x[slices]
            return ifft_obj().copy()

    # Define fft function
    if fft_pair is True:
        fft_obj = pyfftw.FFTW(u, v, direction='FFTW_FORWARD', axes=(axis,))

        if n > nfft:
            raise ValueError("NFFT must be at least equal to signal length "
                             "when returning an FFT pair.")

        elif n < nfft and crop_fft:
            slices[axis] = slice(None, n)

            def planned_fft(x):
                u[:] = x
                return fft_obj().copy()[slices]

        else:
            def planned_fft(x):
                u[:] = x
                return fft_obj().copy()

        return planned_ifft, planned_fft

    else:
        return planned_ifft


def irfft(a, nfft=None, axis=-1, fft_pair=False):
    """Returns a planned function that computes the real-valued 1-D inverse DFT
    of a sequence or array.

    Parameters
    ----------
        a : number, shape or array-like
            An input array, its shape or length.
        nfft : Optional[int]
            Number of FFT points. Default is input size along specified axis
        axis : Optional[int]
            Axis along which to perform the fft. Default is -1.
        fft_pair : Optional[boolean]
            Indicates Whether or not to also return an ifft function. Default
            is False.

    Returns
    -------
        planned_irfft(x)
            Planned ifft function.
        planned_rfft(x)
            Planned fft function. Returned if fft_pair is True.
    """
    # Get shape
    shape = _utils.get_shape(a)
    n = 2*(shape[axis] - 1)

    # Set up slices and pyfftw shapes
    n_dim = len(shape)
    slices = [slice(None)] * n_dim

    if nfft is None:
        nfft = n

    nfft_complex = nfft//2 + 1

    u_shape = list(shape)
    v_shape = list(shape)
    u_shape[axis] = nfft
    v_shape[axis] = nfft_complex

    # Set data types
    if np.asarray(a).dtype.name in ('float32', 'int32', 'complex64'):
        dtype = 'float32'
        fft_dtype = 'complex64'
    else:
        dtype = 'float64'
        fft_dtype = 'complex128'

    u = pyfftw.n_byte_align_empty(u_shape, 16, dtype)
    v = pyfftw.n_byte_align_empty(v_shape, 16, fft_dtype)
    ifft_obj = pyfftw.FFTW(v, u, direction='FFTW_BACKWARD', axes=(axis,))

    # Define ifft function
    if n == nfft:
        def planned_irfft(x):
            v[:] = x
            return ifft_obj().copy()

    elif n < nfft:
        def planned_irfft(x):
            v[:] = _utils.pad_array(x, v_shape)
            return ifft_obj().copy()

    else:
        slices[axis] = slice(0, nfft_complex)

        def planned_irfft(x):
            v[:] = x[slices]
            return ifft_obj().copy()

    # Define ifft function
    if fft_pair is True:
        fft_obj = pyfftw.FFTW(u, v, direction='FFTW_FORWARD', axes=(axis,))

        if n <= nfft:
            def planned_rfft(x):
                u[:] = x
                return fft_obj().copy()
        else:
            raise ValueError("NFFT must be at least equal to signal length "
                             "when returning an FFT pair.")

        return planned_irfft, planned_rfft

    else:
        return planned_irfft


def ifftn(a, shape=None, axes=None, fft_pair=False, crop_fft=False):
    """Returns a planned function that computes the N-D DFT of an array.

    Parameters
    ----------
        a : array-like or shape
            An input array or its shape
        nfft : Optional[sequence of ints]
            Number of FFT points. Default is input size along specified axes
        axes : Optional[sequence of ints]
            Axes along which to perform the fft. Default is all axes.
        fft_pair : Optional[boolean]
            Indicates Whether or not to also return an ifft function. Default
            is False.
        crop_fft : Optional[boolean]
            Indicates that the fft function should crop its output to match
            the shape of the input to the ifft function

    Returns
    -------
        planned_fftn(x)
            Planned fft function.
        planned_ifftn(x)
            Planned ifft function. Returned if fft_pair is True.
    """
    # Get shape of input
    a_shape = _utils.get_shape(a)
    n_dim = len(a_shape)

    if shape is None:
        if axes is None:
            shape = a_shape
        else:
            shape = [a_shape[axis] for axis in axes]

    if axes is None:
        n_dim_s = len(shape)
        dim_diff = n_dim - n_dim_s
        axes = [k + dim_diff for k in range(n_dim_s)]

    # Make sure axes and shape are iterable
    if np.asarray(axes).ndim == 0:
        axes = (axes,)
    if np.asarray(shape).ndim == 0:
        shape = (shape,)

    # Compute FFTW shape
    fft_shape = list(a_shape)
    for n, axis in zip(range(len(axes)), axes):
        fft_shape[axis] = shape[n]

    # Set up slices
    slices = [slice(None)] * n_dim
    for axis in axes:
        slices[axis] = slice(0, fft_shape[axis])

    # Set data type
    if np.asarray(a).dtype.name in ('float32', 'int32', 'complex64'):
        dtype = 'complex64'
    else:
        dtype = 'complex128'

    u = pyfftw.n_byte_align_empty(fft_shape, 16, dtype)
    v = pyfftw.n_byte_align_empty(fft_shape, 16, dtype)
    ifft_obj = pyfftw.FFTW(v, u, direction='FFTW_BACKWARD', axes=axes)

    has_smaller_axis = any(s1 < s2 for s1, s2 in zip(a_shape, fft_shape))
    has_larger_axis = any(s1 > s2 for s1, s2 in zip(a_shape, fft_shape))

    # Define ifft function
    if has_smaller_axis and has_larger_axis:
        def planned_ifftn(x):
            v[:] = _utils.pad_array(x[slices], fft_shape)
            return ifft_obj().copy()

    elif has_larger_axis:
        def planned_ifftn(x):
            v[:] = x[slices]
            return ifft_obj().copy()

    elif has_smaller_axis:
        def planned_ifftn(x):
            v[:] = _utils.pad_array(x, fft_shape)
            return ifft_obj().copy()

    else:
        def planned_ifftn(x):
            v[:] = x
            return ifft_obj().copy()

    # Define fftn function
    if fft_pair is True:
        fft_obj = pyfftw.FFTW(u, v, direction="FFTW_FORWARD", axes=axes)

        if has_larger_axis:
            raise ValueError("Number of FFT points must be equal to or greater"
                             "than the signal length for each axis when "
                             "returning an FFT pair.")

        elif has_smaller_axis and crop_fft:
            for axis in axes:
                slices[axis] = slice(0, a_shape[axis])

            def planned_fftn(x):
                u[:] = x
                return fft_obj().copy()[slices]

        else:
            def planned_fftn(x):
                u[:] = x
                return fft_obj().copy()

        return planned_ifftn, planned_fftn

    else:
        return planned_ifftn


def irfftn(a, shape=None, axes=None, fft_pair=False):
    """Returns a planned function that computes the N-D DFT of a real-valued
    array.

    Parameters
    ----------
        a : array-like or shape
            An input array or its shape.
        nfft : Optional[sequence of ints]
            Number of FFT points. Default is input size along specified axes
        axes : Optional[sequence of ints]
            Axes along which to perform the fft. Default is all axes.
        fft_pair : Optional[boolean]
            Indicates Whether or not to also return an ifft function. Default
            is False.

    Returns
    -------
        planned_rfftn(x)
            Planned fft function.
        planned_irfftn(x)
            Planned ifft function. Returned if fft_pair is True.
    """
    # Get shape of input
    a_shape = _utils.get_shape(a)
    n_dim = len(a_shape)

    if shape is None:
        if axes is None:
            shape = [n for n in a_shape]
            shape[-1] = 2*(shape[-1] - 1)
        else:
            shape = [a_shape[axis] for axis in axes]
            shape[axes[-1]] = 2*(shape[axes[-1]] - 1)
    else:
        shape = list(shape)

    if axes is None:
        n_dim_s = len(shape)
        dim_diff = n_dim - n_dim_s
        axes = [k + dim_diff for k in range(n_dim_s)]

    # Make sure axes and shape are iterable
    if np.asarray(axes).ndim == 0:
        axes = (axes,)
    if np.asarray(shape).ndim == 0:
        shape = (shape,)

    # Compute FFTW shape
    u_shape = list(a_shape)
    v_shape = list(a_shape)

    for n, axis in zip(range(len(axes)), axes):
        u_shape[axis] = shape[n]
        v_shape[axis] = shape[n]

    v_shape[axes[-1]] = v_shape[axes[-1]]//2 + 1

    # Set up slices
    slices = [slice(None)] * n_dim
    for axis in axes:
        slices[axis] = slice(0, v_shape[axis])

    # Set data types
    if np.asarray(a).dtype.name in ('float32', 'int32', 'complex64'):
        dtype = 'float32'
        fft_dtype = 'complex64'
    else:
        dtype = 'float64'
        fft_dtype = 'complex128'

    u = pyfftw.n_byte_align_empty(u_shape, 16, dtype)
    v = pyfftw.n_byte_align_empty(v_shape, 16, fft_dtype)
    ifft_obj = pyfftw.FFTW(v, u, direction='FFTW_BACKWARD', axes=axes)

    has_smaller_axis = any(s1 < s2 for s1, s2 in zip(a_shape, v_shape))
    has_larger_axis = any(s1 > s2 for s1, s2 in zip(a_shape, v_shape))

    # Define ifft function
    if has_smaller_axis and has_larger_axis:
        def planned_irfftn(x):
            v[:] = _utils.pad_array(x[slices], v_shape)
            return ifft_obj().copy()

    elif has_larger_axis:
        def planned_irfftn(x):
            v[:] = x[slices]
            return ifft_obj().copy()

    elif has_smaller_axis:
        def planned_irfftn(x):
            v[:] = _utils.pad_array(x, v_shape)
            return ifft_obj().copy()

    else:
        def planned_irfftn(x):
            v[:] = x
            return ifft_obj().copy()

    # Define ifftn function
    if fft_pair is True:
        fft_obj = pyfftw.FFTW(u, v, direction="FFTW_FORWARD", axes=axes)

        if has_larger_axis:
            raise ValueError("Number of FFT points must be equal to or greater"
                             "than the signal length for each axis when "
                             "returning an FFT pair")

        else:
            def planned_rfftn(x):
                u[:] = x
                return fft_obj().copy()

        return planned_irfftn, planned_rfftn

    else:
        return planned_irfftn
