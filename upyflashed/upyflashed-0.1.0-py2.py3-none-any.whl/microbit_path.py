import psutil

MICROBIT = 'MICROBIT'


def read_psutil():
    partitions = psutil.disk_partitions()
    for partition in partitions:
        mount = partition.mountpoint
        if mount.endswith(MICROBIT):
            return mount

methods = (read_psutil,)

def get_default_microbit_path():
    for method in methods:
        path = method()
        if path:
            return path


if __name__ == '__main__':
    for method in methods:
        path = method()
        print method, path
