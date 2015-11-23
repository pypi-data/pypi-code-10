from setuptools import setup, find_packages

setup(
    name='garforprudence',
    version='0.0.1a3',
    packages = find_packages(),
    url='https://github.com/tychenjiajun',
    license='MIT License',
    keywords='python gmail',
    author='tychenjiajun',
    author_email='tychenjiajun@163.com',
    description='An example distribution',
    install_requires=[
        'google-api-python-client'
    ],
    scripts = ['GmailAutoReply.py'],
    entry_points={
        'console_scripts':[
        'GmailAutoReply = GmailAutoReply:main'
    ]},
)
