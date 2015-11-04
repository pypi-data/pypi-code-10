from distutils.core import setup

setup(
    name='GithubUsers',
    version='0.1.0',
    author='Yanko Bolanos',
    author_email='y@rem7.com',
    packages=[],
    scripts=['bin/github_users'],
    url='https://github.com/rem7/GithubUsers',
    license='LICENSE.txt',
    description="Add a team's user ssh keys to a global user",
    long_description=open('README.txt').read(),
    install_requires=[
        "requests>=2.2.1",
    ],
)
