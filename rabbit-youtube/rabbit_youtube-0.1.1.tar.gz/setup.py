from setuptools import setup

setup(name='rabbit_youtube',
      version='0.1.1',
      description='rabbit youtube utils',
      author='Guoliang Li',
      author_email='dev@liguoliang.com',
      url='http://rabbitsrc.com/youtube',
      packages=['rabbit_youtube'],
      scripts=['scripts/rabbit-youtube.py'],
      license='Apache Software License',
      install_requires=['pytube']
     )