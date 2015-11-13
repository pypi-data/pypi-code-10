from setuptools import setup


try:
    long_description = open('README.rst').read()
except:
    long_description = 'Nana keeps an eye on a directory and reacts when anything changes.'


setup(
    name='nana',
    version='1.0.1',
    author='Konstantin Molchanov',
    description='Nana keeps an eye on a directory and reacts when anything changes',
    long_description=long_description,
    author_email='moigagoo@live.com',
    url='https://bitbucket.org/moigagoo/nana',
    py_modules=['nana'],
    install_requires=['cliar'],
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix'],
    entry_points={
        'console_scripts': [
            'nana=nana:main'
        ]
    }
)
