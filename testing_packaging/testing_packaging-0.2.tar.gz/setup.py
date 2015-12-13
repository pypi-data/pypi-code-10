from setuptools import setup
#This is a list of files to install, and where
#(relative to the 'root' dir, where setup.py is)
#You could be more specific.
# files = ["things/*"]

# setup(name = "testing_packaging",
#     version = "100",
#     description = "Testing packaging",
#     author = "Zia",
#     author_email = "email@someplace.com",
#     url = "whatever",
#     #Name the folder where your packages live:
#     #(If you have other packages (dirs) or modules (py files) then
#     #put them into the package directory - they will be found
#     #recursively.)
#     packages = ['package'],
#     #'package' package must contain files (see list above)
#     #I called the package 'package' thus cleverly confusing the whole issue...
#     #This dict maps the package name =to=> directories
#     #It says, package *needs* these files.
#     package_data = {'package' : files },
#     #'runner' is in the root.
#     scripts = ["runner"],
#     long_description = """Really long text here."""
#     #
#     #This next part it for the Cheese Shop, look a little down the page.
#     #classifiers = []
# )
setup(name='testing_packaging',
      version='0.2',
      description='The funniest joke in the world',
      url='http://github.com/storborg/funniest',
      author='Flying Circus',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=['testing_packaging'],
      install_requires=[
          'bibtexparser','gitpython'
      ],      
      test_suite='nose.collector',
      tests_require=['nose'],
      scripts=['bin/runner'],      
      zip_safe=False)