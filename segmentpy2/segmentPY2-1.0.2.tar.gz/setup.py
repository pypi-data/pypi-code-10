from setuptools import setup, Extension
module1 = Extension('segmentPY2',
        sources = ['segmentPY.cpp','../segment/WordData.cpp','../segment/DATrieDict.cpp','../segment/WordSplit.cpp','../segment/WordSplitter.cpp'],
        include_dirs=['../segment'],
        libraries = ['pthread'],
        library_dirs = ['/usr/local/lib']
        )

setup(
    name="segmentPY2",
    version = "1.0.2",
    author = "lihaifeng",
    ext_modules = [module1]
)
