
import os, pip

# from pip.req import parse_requirements

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def read_version():
    with open(os.path.join(os.path.dirname(__file__), 'recorder/__init__.py')) as f:
        for line in f:
            if 'VERSION' in line:
                version = line.split('=')[1].replace("\"", "").strip()
                return version

install_reqs = pip.req.parse_requirements('requirements.txt', session=pip.download.PipSession())

requirements = [str(ir.req) for ir in install_reqs if ir is not None]

setup(name             = "ece-recorder",
      author           = "Aljosha Friemann",
      author_email     = "aljosha.friemann@gmail.com",
      license          = "",
      version          = read_version(),
      description      = "EclipseConEurope recording script",
      url              = "www.bitbucket.org/afriemann/ece-recorder.git",
      keywords         = [],
      # download_url     = "",
      install_requires = requirements,
      long_description = read('README.rst'),
      classifiers      = [],
      packages         = ["recorder"],
      scripts          = ["scripts/recorder"]
)
