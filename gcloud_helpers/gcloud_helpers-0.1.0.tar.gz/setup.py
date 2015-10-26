from distutils.core import setup

setup(
  name='gcloud_helpers',
  version='0.1.0',
  author='Yonatan Kogan',
  author_email='yonatan@optimizely.com',
  packages=['gcloud_helpers'],
  url='https://github.com/optimizely/gcloud-helpers',
  license='Copyright Optimizely',
  description='Helper files for interacting the the GCloud API',
  long_description=open('README.md').read(),
  install_requires=[
    # "gcloud" commented out b/c can't specify a commit hash
  ],
)