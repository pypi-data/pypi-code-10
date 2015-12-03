from setuptools import setup

setup(
    name='d3smush',
    version='0.1',
    py_modules=['smusher'],
    include_package_data=True,
    install_requires=[
        'requests',
        'clint'
    ],
    entry_points='''
        [console_scripts]
        d3smush=smusher:main
    ''',
    description = 'Library to smush together D3 components in the right order',
    author = 'Kshitij Aranke',
    author_email = 'kshitij.aranke@gmail.com',
    url = 'https://github.com/xaranke/d3smush',
    download_url = 'https://github.com/xaranke/d3smush/tarball/0.1',
    keywords = ['d3', 'smush', 'javascript'],
    classifiers = [],
)
