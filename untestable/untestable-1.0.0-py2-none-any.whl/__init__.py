import sys
from untestable.di.console_config import APP


def main():
    """Entry point for the application script"""
    APP.run(sys.argv[1:])
