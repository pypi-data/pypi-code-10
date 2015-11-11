from distutils.core import setup

def readme():
    with open('README.txt') as f:
        return f.read()

def license():
    with open('License_notice.txt') as f:
        return f.read()

    with open('GNU_GPL.txt') as f:
        return f.read()

setup(
    name='pyplotwrap',
    version='0.23beta',
    packages=['pyplotwrap',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
    url='https://github.com/nenanth/python_plot_wrappers',
    author='Ananth Sridharan',
    author_email='sridharan.ananth@gmail.com',
)
