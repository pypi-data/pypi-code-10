# -*- coding: utf8 -*-

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import string
import random

def setup_func():
    key = read_test_key()
    return [key], {}


def read_test_key():
    f = open(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "api.key")), "r")
    try:
        return f.read().strip()
    finally:
        f.close()


def with_setup_args(setup, teardown=None):
    """Decorator to add setup and/or teardown methods to a test function::
      @with_setup_args(setup, teardown)
      def test_something():
          " ... "
    The setup function should return (args, kwargs) which will be passed to
    test function, and teardown function.
    Note that `with_setup_args` is useful *only* for test functions, not for test
    methods or inside of TestCase subclasses.

    From C{https://gist.github.com/garyvdm/392ae20c673c7ee58d76}
    """

    def decorate(func):
        args = []
        kwargs = {}

        def test_wrapped():
            func(*args, **kwargs)

        test_wrapped.__name__ = func.__name__

        def setup_wrapped():
            a, k = setup()
            args.extend(a)
            kwargs.update(k)
            if hasattr(func, 'setup'):
                func.setup()

        test_wrapped.setup = setup_wrapped

        if teardown:
            def teardown_wrapped():
                if hasattr(func, 'teardown'):
                    func.teardown()
                teardown(*args, **kwargs)

            test_wrapped.teardown = teardown_wrapped
        else:
            if hasattr(func, 'teardown'):
                test_wrapped.teardown = func.teardown()
        return test_wrapped

    return decorate


def random_string(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
