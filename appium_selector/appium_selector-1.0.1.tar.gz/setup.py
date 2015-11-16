from setuptools import setup
setup(
  name = 'appium_selector',
  packages = ['appium_selector'],
  version = '1.0.1',
  include_package_data = True,
  description = 'Creates a Tcl/Tk window to read connected Appium devices from Selenium Grid and display them for selection',
  author = 'Matt Watson',
  author_email = 'Watson.Mattc@gmail.com',
  url = 'https://github.com/Mattwhooo/appium_selector.git',
  download_url = 'https://github.com/Mattwhooo/appium_selector/tarball/1.0.1',
  keywords = ['appium', 'selenium', 'testing'],
  classifiers=[],
  install_requires=['beautifulsoup4', 'requests']
)