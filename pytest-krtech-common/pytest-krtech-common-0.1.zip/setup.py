from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='pytest-krtech-common',
      version='0.1',
      description='pytest krtech common library',
      long_description=readme(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.4',
          'Environment :: Plugins',
          'Topic :: Software Development :: Testing',
      ],
      author='Maksim Filippov',
      author_email='m.filippov@krtech.ru',
      license='MIT',
      packages=['steps', 'elements'],
      install_requires=[
          'pytest', 'selenium', 'pyhamcrest', 'pytest-allure-adaptor', 'sqlalchemy', 'mysqlclient'
      ],
      zip_safe=False)
