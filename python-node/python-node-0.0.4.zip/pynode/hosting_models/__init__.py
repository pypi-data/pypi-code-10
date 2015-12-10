from .http_node_instance import *
from .io_node_instance import *
from enum import Enum


class HostingModel(Enum):
    http = 0
    stream = 1
