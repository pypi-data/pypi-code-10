try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='historist',
      version='0.1.0.dev2',
      description='activity logger',
      url='http://github.com/sina33/historist',
      author='Sina Saeedi',
      author_email='sina.saeedi@outlook.com',
      license='MIT',
      keywords="archive events logs".split(),
      packages=['historist'],
      install_requires=[
          "sqlalchemy>=1.0.9"
      ],
      entry_points={
          "console_scripts": [
              "histopush = historist:histopush",
              "histoplay = historist:histoplay",
              "historist = historist:historist"
          ]
      },
      zip_safe=False)
