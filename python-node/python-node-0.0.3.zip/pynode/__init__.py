from .hosting_models import HttpNodeInstance, IONodeInstance, HostingModel

__version__ = '0.0.3'


def create_node_service(service_hosting_model, root_path, *args, **kwargs):
    if service_hosting_model == HostingModel.http:
        return HttpNodeInstance(root_path, *args, **kwargs)
    elif service_hosting_model == HostingModel.stream:
        return IONodeInstance(root_path, *args, **kwargs)
    else:
        raise KeyError('Unknown hosting model ' + str(service_hosting_model))
