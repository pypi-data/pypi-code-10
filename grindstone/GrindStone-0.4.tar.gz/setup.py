from distutils.core import setup

setup(
    name='GrindStone',
    version='0.4',
    packages=['grindstone'],
    author='Elijah Caine',
    author_email='elijahcainemv@gmail.com',
    url='http://github.com/elijahcaine/GrindStone',
    description='Helping you put your nose to the GrindStone since 2015.',
    scripts=['grindstone/grindstone'],
    license='MIT',
    classifiers=[
      'Programming Language :: Python :: 3',
      'License :: OSI Approved :: MIT License',
      'Development Status :: 4 - Beta',
    ],
    keywords='todo grindstone tasks lists',
    download_url='https://github.com/ElijahCaine/GrindStone/archive/master.zip'
)
