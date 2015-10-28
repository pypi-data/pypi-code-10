# Copyright (c) 2015 Luke Pinner
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

'''
Simple [usercustomize.py][1] to keep separate ```site.USER_BASE/USER_SITE```
directories for 32 and 64bit python installs on Windows.
    
Only required if you're installing extension modules (compiled pyd/dll)
to the [user site-packages directory][2], i.e.:

    python setup.py install --user
    pip install --user somepackage
    
Save to %AppData%\Roaming\Python\Python27\site-packages\usercustomize.py

[1]: https://docs.python.org/2/library/site.html
[2]: https://docs.python.org/2/install/index.html#inst-alt-install-user
'''

import os, site, sys

if sys.maxsize > 2**32: # 64 bit
    old_user_base = site.USER_BASE
    site.USER_BASE = site.USER_BASE + '-x64'
    site.USER_SITE = site.USER_SITE.replace(old_user_base, site.USER_BASE)
    if not os.path.exists(site.USER_SITE):
        os.makedirs(site.USER_SITE)
    site.addsitedir(site.USER_SITE, known_paths=[])
    for i, path in enumerate(sys.path[:]):
        if old_user_base in path:
            sys.path.remove(path)
            new_path = path.replace(old_user_base, site.USER_BASE)
            if os.path.exists(new_path):
                sys.path.insert(i, new_path)
                
    if site.USER_SITE not in sys.path:
        sys.path.insert(0, site.USER_SITE)
