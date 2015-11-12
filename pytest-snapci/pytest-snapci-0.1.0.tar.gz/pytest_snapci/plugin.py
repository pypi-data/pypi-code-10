
import os, hashlib


class SnapCIError(Exception):
    """Raised for problems running the Snap-CI py.test plugin"""


def read_circleci_env_variables():
    """Read and convert SNAP_* environment variables"""
    snap_node_total = int(os.environ.get("SNAP_WORKER_TOTAL", "1").strip())
    snap_node_index = int(os.environ.get("SNAP_WORKER_INDEX", "0").strip())

    if snap_node_index >= snap_node_total:
        raise SnapCIError("SNAP_WORKER_INDEX={} >= SNAP_WORKER_TOTAL={}, should be less".format(snap_node_index, snap_node_total))

    return (snap_node_total, snap_node_index)


def pytest_report_header(config):
    """Add Snap-CI information to report"""
    snap_node_total, snap_node_index = read_circleci_env_variables()
    return "Snap-CI total nodes: {}, this node index: {}".format(snap_node_total, snap_node_index)


def pytest_collection_modifyitems(session, config, items):
    """
    Use Snap-CI env vars to determine which tests to run

    - SNAP_WORKER_TOTAL indicates total number of nodes tests are running on
    - SNAP_WORKER_INDEX indicates which node this is

    Will run a subset of tests based on the node index.

    """
    snap_node_total, snap_node_index = read_circleci_env_variables()
    deselected = []
    for index, item in enumerate(list(items)):
        item_hash = int(hashlib.sha1(':'.join(map(str, item.location))).hexdigest(), 16)
        if (item_hash % snap_node_total) != snap_node_index:
            deselected.append(item)
            items.remove(item)
    config.hook.pytest_deselected(items=deselected)
