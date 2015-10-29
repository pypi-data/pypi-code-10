#!/usr/bin/env python
"""
Echo the s3s3 supervisord configuration file.
"""
import logging
from pkg_resources import Requirement, resource_string


def echo():
    """
    Echo the s3s3 supervisord configuration file.
    """
    try:
        conf = resource_string(Requirement.parse('s3s3'),
                               'extras/s3s3.conf')
        print(conf.decode('utf-8'))
        return True
    except Exception:
        return False


def main():
    if echo():
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
