import os
import sys
from setuptools import setup

# pybashcomplete
# Bash completion utility for python scripts


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "pybashcomplete",
    version = "0.0.2",
    description = "Bash completion utility for python scripts",
    author = "Johan Nestaas",
    author_email = "johannestaas@gmail.com",
    license = "GPLv3+",
    keywords = "",
    url = "https://www.bitbucket.org/johannestaas/pybashcomplete",
    packages=['pybashcomplete'],
    package_dir={'pybashcomplete': 'pybashcomplete'},
    long_description=read('README.rst'),
    classifiers=[
        #'Development Status :: 1 - Planning',
        #'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        #'Development Status :: 6 - Mature',
        #'Development Status :: 7 - Inactive',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Environment :: MacOS X',
        #'Environment :: Win32 (MS Windows)',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        #'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
    ],
    install_requires=[
    ],
    entry_points = {
        'console_scripts': [
            'pybashcomplete = pybashcomplete:main',
        ],
    },
    #package_data = {
        #'pybashcomplete': ['catalog/*.edb'],
    #},
    #include_package_data = True,
)

BASHCOMPLETE_CONFIG = '''#-*- mode: shell-script;-*-

# Debian GNU/Linux python completion

_python()
{
    pybash=`pybashcomplete $COMP_LINE`
    if [[ $pybash =~ COMPLETE:(.+) ]] ; then
        COMPREPLY="${BASH_REMATCH[1]}"
    elif [[ $pybash =~ MULTIPLE:(.+) ]] ; then
        COMPREPLY=(${BASH_REMATCH[1]})
    fi
}
'''

if os.path.isdir('/etc/bash_completion.d'):
    try:
        with open('/etc/bash_completion.d/pybashcomplete', 'w') as f:
			f.write(BASHCOMPLETE_CONFIG)
    except Exception:
        import traceback
        traceback.print_exc()
        sys.stderr.write('Exception occurred on installation.\n'
                         'You need to install with sudo or root.\n')
else:
    sys.stderr.write('/etc/bash_completion.d directory not found.\n'
                     'Installation failed. If your environment places bash '
                     'completion scripts in a different area, paste this '
                     'script there: \n' + BASHCOMPLETE_CONFIG)
