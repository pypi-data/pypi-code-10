#! python3

from distutils.core import setup

setup(name='Mind',
        version='0.3.1',
        author='Jakov Manjkas',
        author_email='jakov.manjkas@gmail.com',
        url='https://github.com/Knowlege/Mind',
        description='Mind is library for games in Python',
        keywords ='pygame game tiled',
        long_description="""\
Mind is divided on four parts (for now): Mind.Knowledge, Mind.Orientation, Mind.Imagination and Mind.Existence (and Mind.Test but it's only for testing).\n
Next version will be 0.3.2\n
In that version I'm adding new stuff to Existence.\n
For help see Documentation, Tutorial, use Mind. Tets file (and try to understand its code) and see pro files.\n
Notes: Documentation on PYPI might be late and Mind is Python 2 incompatible!
""",
        packages = ['Mind', 'Mind/pro/Orientation', 'Mind/pro', 'Mind/pro/Imagination', 'Mind/pro/Existence'],
        package_data={"Mind":
        ["Documentation/*.html", "Documentation/*.js", "Documentation/*.inv", "Documentation/_sources/*", "Documentation/_static/*",
         "Documentation/_modules/*.html", "Documentation/_modules/Mind/*"]
        },
        classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment'
        ]
)
