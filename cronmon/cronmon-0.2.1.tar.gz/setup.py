import setuptools
import versioneer

setuptools.setup(
    name="cronmon",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    url="https://github.com/malev/cronmon",

    author="Marcos Vanetta",
    author_email="marcosvanetta@gmail.com",
    description="Monitor your crontasks",
    long_description=open('README.md').read(),
    packages=setuptools.find_packages(),
    scripts=['bin/cronmon'],
    install_requires=['click', 'flask', 'jinja2'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
