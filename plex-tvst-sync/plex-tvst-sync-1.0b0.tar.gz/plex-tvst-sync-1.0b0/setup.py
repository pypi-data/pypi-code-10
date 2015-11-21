import ez_setup
ez_setup.use_setuptools()

from distutils.command.install import install
from setuptools import setup


class CustomInstall(install):
    def _setup_cron(self):
        import crontab
        
        cron = crontab.CronTab(user=True)
        job = cron.new(command='plex-tvst-sync')
        job.setall('@hourly')
        cron.write_to_user(user=True)
    
    def run(self):
        install.run(self)
        self._setup_cron()


setup(
    name='plex-tvst-sync',
    version='1.0b',
    author='sprt',
    author_email='hellosprt@gmail.com',
    url='https://github.com/sprt/plex-tvst-sync',
    keywords='plex tvshowtime scrobbler sync',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2 :: Only',
    ],
    cmdclass={'install': CustomInstall},
    setup_requires=[
        'python-crontab==1.9.3',
    ],
    install_requires=[
        'appdirs==1.4.0',
        'PlexAPI==1.1.0',
        'python-crontab==1.9.3',
        'requests==2.8.1',
    ],
    entry_points={'console_scripts': ['plex-tvst-sync = scrobbler:main']},
)
