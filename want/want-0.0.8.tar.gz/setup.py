from setuptools import setup


setup(
    name='want',
    version='0.0.8',
    description='Download images from website.',
    author='YogaPan',
    author_email='godhand1234567@gmail.com',
    packages=['want'],
    py_modules=['wantFrom'],
    scripts=['scripts/want'],
    install_requires=['requests', 'BeautifulSoup4'],
    url='https://github.com/YogaPan/want',
    download_url=''
)
