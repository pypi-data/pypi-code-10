from setuptools import setup


setup(name='django_mail_save',
      version='0.0.5',
      packages=['mail_save'],
      description='Save outgoing mail to the database',
      long_description=open('README.rst').read(),
      url='https://github.com/bigmassa/django_mail_save',
      author='Stuart George',
      author_email='stuart.bigmassa@gmail.com',
      license='MIT',
      keywords = ['mail', 'save', 'email', 'admin'],
      install_requires=[
            'Django>=1.8,<1.9.99',
      ],
      include_package_data=True,
      classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Web Environment',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.5',
            'Topic :: System :: Logging',
            'Topic :: Communications :: Email',
      ],
)
