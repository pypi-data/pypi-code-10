from data_manager import DataManager


def get_version():
    from pkg_resources import get_distribution, DistributionNotFound

    try:
        version = get_distribution(__name__).version
    except DistributionNotFound:
        version = "unknown, try running `python setup.py egg_info`"

    return version


__version__ = get_version()

__all__ = ['__version__', 'DataManager']
