
import os, hashlib


class SnapCIError(Exception):
    """Raised for problems running the Snap-CI py.test plugin"""


def read_snapci_env_variables():
    """Read and convert SNAP_* environment variables"""
    snap_worker_total = int(os.environ.get("SNAP_WORKER_TOTAL", "1").strip())
    snap_worker_index = int(os.environ.get("SNAP_WORKER_INDEX", "1").strip())

    if snap_worker_index > snap_worker_total:
        raise SnapCIError("SNAP_WORKER_INDEX={} >= SNAP_WORKER_TOTAL={}, should be less".format(snap_worker_index, snap_worker_total))

    return (snap_worker_total, snap_worker_index)


def pytest_report_header(config):
    """Add Snap-CI information to report"""
    snap_worker_total, snap_worker_index = read_snapci_env_variables()
    return "Snap-CI total nodes: {}, this node index: {}".format(snap_worker_total, snap_worker_index)


def pytest_collection_modifyitems(session, config, items):
    """
    Use Snap-CI env vars to determine which tests to run

    - SNAP_WORKER_TOTAL indicates total number of nodes tests are running on
    - SNAP_WORKER_INDEX indicates which node this is

    Will run a subset of tests based on the node index.

    """
    if os.environ.get("SNAP_CI", False) != "true":
        return
    snap_worker_total, snap_worker_index = read_snapci_env_variables()
    deselected = []
    for index, item in enumerate(list(items)):
        item_hash = int(hashlib.sha1(u':'.join(map(str, item.location)).encode('utf-8')).hexdigest(), 16)
        if (item_hash % snap_worker_total) != snap_worker_index:
            deselected.append(item)
            items.remove(item)
    config.hook.pytest_deselected(items=deselected)
