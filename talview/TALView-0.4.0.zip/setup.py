from distutils.core import setup
import re

version_re=re.compile("^__version__ *= *(.+)$")
with open("talview.py","r") as f:
    for line in f:
        m=version_re.match(line)
        if m:
            __version__=eval(m.group(1))
            break

setup(
    name='TALView',
    version=__version__,
    author='Jan Brohl',
    author_email='janbrohl@t-online.de',
    url='https://bitbucket.org/janbrohl/talview',
    license='BSD-3-clause',
    description="TAL-Templates as Views",
    py_modules=['talview'],
    requires=["simpletal (>=4.3)"],
)
