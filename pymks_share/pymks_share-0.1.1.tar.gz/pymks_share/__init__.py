from data_manager import DataManager


def fetch_data(dataset_name):
    """fetches data from server

    Args:
        dataset_name (str): Name of dataset

    returns:
        tuple of structure data and response data
    """
    manager = DataManager()
    return manager.fetch_data(dataset_name)


def list_data():
    """list datasets on server

    returns:
        list of all dataset names
    """
    manager = DataManager()
    return manager.list_dataset_names()


def push_data(dataset_name, structure_data, data_source, parameters,
              response_data=None, authors=None, description=None,
              other_metadata=None):
    """push data up to server

    Args:
        dataset_name (str): name of dataset
        structure_data (ND array): materials structure data
        data_source (str): information about source of data
        parameters (dict): parameters used to create the data
        response_data (ND array, optional): materials response data
        authors (str, optional): authors
        description (str, optional): description of dataset
        other_metadata (str, optional): other metadata
    """
    manager = DataManager()
    manager.push_data(dataset_name, structure_data, data_source,
                      parameters, response_data=response_data,
                      authors=authors, description=description,
                      other_metadata=other_metadata)


def get_version():
    from pkg_resources import get_distribution, DistributionNotFound

    try:
        version = get_distribution(__name__).version
    except DistributionNotFound:
        version = "unknown, try running `python setup.py egg_info`"

    return version


__version__ = get_version()

__all__ = ['__version__', 'fetch_data', 'DataManager', 'list_data',
           'push_data']
