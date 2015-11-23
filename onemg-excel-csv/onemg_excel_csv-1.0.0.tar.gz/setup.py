from setuptools import setup
from os import path, getcwd

if not path.dirname(__file__):  # setup.py without /path/to/
    _dirname = getcwd()  # /path/to/
else:
    _dirname = path.dirname(path.dirname(__file__))


def read(name, default=None, debug=True):
    try:
        filename = path.join(_dirname, name)
        with open(filename) as f:
            return f.read()
    except Exception as e:
        err = "%s: %s" % (type(e), str(e))
        if debug:
            print(err)
        return default


def lines(name):
    txt = read(name)
    return map(
        lambda l: l.lstrip().rstrip(),
        filter(lambda t: not t.startswith('#'), txt.splitlines() if txt else [])
    )


install_requires = [i for i in lines("requirements.txt") if '-e' not in i]

setup(name='onemg_excel_csv',
      version='1.0.0',
      author='Om Jangir',
      author_email='omjangir2006@gmail.com',
      description='onemg_excel_csv library which uses ',
      packages=['onemg_excel_csv'], install_requires=install_requires)
