from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='prettyrecord',
      version='0.1',
      description="Structures like SQLAlchemy's declarative_base or Django's models in your project!",
      long_description=readme(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Libraries',
          'Intended Audience :: Developers'
      ],
      keywords='structure model declarative record',
      url='http://github.com/skorczan/prettyrecord',
      author='Andrzej Skórcz',
      author_email='skorczan@gmail.com',
      license='MIT',
      packages=['prettyrecord'])