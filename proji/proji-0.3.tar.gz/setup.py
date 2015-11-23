from setuptools import setup

setup(name='proji',
      version='0.3',
      author="Markus Binsteiner",
      author_email="makkus@gmail.com",
      install_requires=[
          "argparse",
          "requests",
          "restkit",
          "booby",
          "simplejson",
          "parinx",
	  "pyclist"
      ],
      packages=["proji"],
      entry_points={
          'console_scripts': [
              'proji = proji.proji:run'
          ],
      },
      description="Project management helper"
)
