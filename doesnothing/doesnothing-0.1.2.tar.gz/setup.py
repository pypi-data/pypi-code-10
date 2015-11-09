from setuptools import setup

setup(name='doesnothing',
      version='0.1.2',
      description='This does nothing',
      url='http://github.com/dlrice/doesnothing',
      author='Dan Rice',
      author_email='dr9@sanger.ac.uk',
      license='MIT',
      packages=['doesnothing'],
      install_requires = [
        'markdown',
      ],
      zip_safe=False)