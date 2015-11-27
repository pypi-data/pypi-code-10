from __future__ import (unicode_literals, division,
                        absolute_import, print_function)


from reggae.build import Target, Build, DefaultOptions  # noqa
from reggae.rules import link, object_files, static_library, scriptlike, target_concat  # noqa

user_vars = dict()


def set_user_vars(new_vars):
    global user_vars
    user_vars = new_vars
