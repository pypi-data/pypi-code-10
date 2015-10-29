#!/usr/bin/env python
"""
Echo the s3s3 configuration template.
"""
import logging
from os.path import abspath, join, dirname, pardir
from pkg_resources import Requirement, resource_string


def echo():
    """
    Echo the s3s3 configuration file in.
    """
    try:
        print(__name__)
        conf = resource_string(Requirement.parse('s3s3'),
                               'extras/s3s3.ini.dist')
        print(conf.decode('utf-8'))
        return True
    except Exception as e:
        print(e)
        return False


def main():
    if echo():
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
