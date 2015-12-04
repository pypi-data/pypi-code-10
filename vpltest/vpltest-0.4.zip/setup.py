from setuptools import setup

setup(
      name="vpltest",
      version=0.4,
      description="Allows running Python tests (unittest, nose, pytest) in the context of VPL Moodle plugin (http://vpl.dis.ulpgc.es/)",
      url="https://bitbucket.org/plas/vpltest",
      license="GPLv3",
      classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: Freeware",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Education",
        "Topic :: Software Development",
        "Topic :: Software Development :: Testing",
      ],
      keywords="pytest nose VPL",
      py_modules=["vpltest"],
)