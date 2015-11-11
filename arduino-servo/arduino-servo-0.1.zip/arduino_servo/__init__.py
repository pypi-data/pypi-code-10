import os

from path_helpers import path


def get_includes():
    import arduino_servo
    r"""
    Return the directory that contains the `arduino_servo` Cython *.hpp and
    *.pxd header files.

    Extension modules that need to compile against `arduino_servo` should use
    this function to locate the appropriate include directory.

    Notes
    -----
    When using ``distutils``, for example in ``setup.py``.
    ::

        import arduino_servo
        ...
        Extension('extension_name', ...
                  include_dirs=[...] + arduino_servo.get_includes())
        ...

    """
    return [os.path.join(os.path.dirname(arduino_servo.__file__), 'Arduino', 'Servo')]

def get_sources():
    '''
    Return Arduino source file paths.  This includes any supplementary source
    files that are not contained in Arduino libraries.
    '''
    return path(get_includes()[0]).files('*.c*')
