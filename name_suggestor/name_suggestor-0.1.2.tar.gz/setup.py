from distutils.core import setup

setup(
    name='name_suggestor',
    packages=['name_suggestor'],
    version='0.1.2',
    description='Suggests a name based on other names found in the US census',
    author='Alex Kahan',
    author_email='alexk307@gmail.com',
    url='https://github.com/alexk307/last_name',
    download_url='https://github.com/alexk307/last_name',
    install_requires=['metaphone'],
    include_package_data=True,
    keywords=['name', 'census', 'recommendation'],
    classifiers=[],
)
