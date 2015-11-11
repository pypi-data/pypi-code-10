from distutils.core import setup

def readme():
    with open('README.rst') as f:
        for line in f:
            print line.rstrip('\n'),'\n'

def license():
   with open('License_notice.txt') as f:
       return f.read()
   with open('GNU_GPL.txt') as f:
       return f.read()

setup(
    name='pyplotwrap',
    version='0.28beta',
    packages=['pyplotwrap',],
    license=license(),
    description='A way to plot data directly from python dictionaries',
    long_description=readme(),
    url='https://github.com/nenanth/python_plot_wrappers',
    author='Ananth Sridharan',
    author_email='sridharan.ananth@gmail.com',
)
