from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='doesnothing',
      version='0.1.5.1',
      description='This does nothing',
      url='http://github.com/dlrice/doesnothing',
      author='Dan Rice',
      author_email='dr9@sanger.ac.uk',
      license='MIT',
      packages=['doesnothing'],
      install_requires=[
        'markdown',
      ],
      entry_points={
        'console_scripts': ['donothing = doesnothing.command_line:main'],
      },
      package_data={
        'doesnothing': ['data.txt']
      })