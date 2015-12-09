"""
Resystem common service package.
Released under New BSD License.
Copyright © 2015, Vadim Markovtsev :: Angry Developers LLC
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the Angry Developers LLC nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL VADIM MARKOVTSEV BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
# Portions of code were extracted from from https://github.com/Samsung/veles


from collections import defaultdict
import json
import logging
import os
from pprint import pprint
import sys

from .argument_parser import get_argument_parser

r = None
__protected__ = defaultdict(set)
__initialized__ = False


class Config(object):
    """Config service class.
    """
    def __init__(self, path):
        self.__path__ = path

    def __del__(self):
        if __protected__ is not None and self in __protected__:
            del __protected__[self]

    def get(self, name, default):
        return self.__content__.get(name, default)

    def update(self, value):
        if self == r and __initialized__:
            raise ValueError("Root updates are disabled")
        if not isinstance(value, (dict, Config)):
            raise ValueError("Value must be an instance of dict or Config")
        self.__update__(
            value if isinstance(value, dict) else value.__content__)
        return self

    def protect(self, *names):
        """
        Makes the specified children names readonly.
        :param names: The names of sub-nodes to restrict modification of.
        """
        __protected__[self].update(names)

    def print_(self, indent=1, width=80, file=sys.stdout):
        def fix_contents(obj):
            fixed_contents = content = obj.__content__
            for k, v in content.items():
                if isinstance(v, Config):
                    fixed_contents[k] = fix_contents(v)
            return fixed_contents

        print('-' * width, file=file)
        print('Configuration "%s":' % self.__path__, file=file)
        pprint(fix_contents(self), indent=indent, width=width, stream=file)
        print('-' * width, file=file)
        sys.stdout.flush()

    def __update__(self, tree):
        for k, v in tree.items():
            if isinstance(v, dict) and not v.get("dict", False):
                getattr(self, k).__update__(v)
            else:
                if isinstance(v, dict) and "dict" in v:
                    del v["dict"]
                setattr(self, k, v)

    def __getattr__(self, name):
        if name in ("__copy__", "__deepcopy__",):
            raise AttributeError()
        if name in ("keys", "values"):
            return getattr(self.__content__, name)
        temp = Config("%s.%s" % (self.__path__, name))
        setattr(self, name, temp)
        return temp

    def __setattr__(self, name, value):
        if name in __protected__[self]:
            raise AttributeError(
                "Attempted to change the protected configuration setting %s.%s"
                % (self.__path__, name))
        super(Config, self).__setattr__(name, value)

    @property
    def __content__(self):
        attrs = dict(self.__dict__)
        if "__path__" in attrs:
            del attrs["__path__"]
        return attrs

    def __repr__(self):
        return '<Config "%s": %s>' % (self.__path__, repr(self.__content__))

    def __getstate__(self):
        """
        Do not remove this method, if you think the default one works the same.
        It actually raises "Config object is not callable" exception.
        """
        return self.__dict__

    def __setstate__(self, state):
        """
        Do not remove this method, if you think the default one works the same.
        It actually leads to "maximum recursion depth exceeded" exception.
        """
        self.__dict__.update(state)

    def __iter__(self):
        return iter(self.__content__)

    def __getitem__(self, item):
        return getattr(self, item)


r = Config("root")
CONFIG_FILE_NAME = "cfg"


def init_argument_parser(parser):
    parser.add_argument("-c", "--configuration", default="", dest="cfgfile",
                        help="path to the configuration file")
    parser.add_argument("overrides", nargs='*', metavar="key=value")
    return parser


def apply_config(path):
    with open(path, "r") as fin:
        r.update(json.load(fin))


def initialize():
    global r
    logger = logging.getLogger("Config")
    for path in os.path.join("/etc", "default", "res", "accounting"), \
            os.path.join(os.path.expanduser("~"), "res", "accounting"), \
            os.getenv("RES_CONFIG"):
        if not path:
            continue
        cfgpath = os.path.join(path, "%s.json" % CONFIG_FILE_NAME)
        if not os.path.exists(cfgpath):
            continue
        try:
            apply_config(cfgpath)
        except Exception as e:
            logger.warning("Failed to configure from %s: %s", cfgpath, e)
    parser = init_argument_parser(get_argument_parser())
    args, _ = parser.parse_known_args()
    if args.cfgfile:
        try:
            apply_config(args.cfgfile)
        except Exception as e:
            logger.critical("Failed to apply configuration from %s: %s",
                            args.cfgfile, e)
            raise e from None
    try:
        exec("\n".join(args.overrides))
    except Exception as e:
        logger.error("Failed to override configuration: %s", e)
    global __initialized__
    __initialized__ = True
    if logging.getLogger("Config").isEnabledFor(logging.DEBUG):
        r.print_()
