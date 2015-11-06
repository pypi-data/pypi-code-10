from .cmd import Cmd


def execute_gensend():
    """ This is called from setup tools as well as local dev bin."""
    Cmd().run()
