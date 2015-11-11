from setuptools import setup

setup(name='piscan',
      version='0.1',
      description='RXWave.com Uniden DMA Police Scanner RaspberryPi agent',
      url='http://www.rxwave.com',
      author='Dave Kolberg',
      author_email='dave.kolberg@gmail.com',
      license='MIT',
      packages=['piscan'],
      install_requires=['pika','boto'],
      zip_safe=False)
