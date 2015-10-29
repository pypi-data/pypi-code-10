"""
handle paths for boost python package
"""

name = 'boostpython'
description = 'boost python'


testcode = '''
#include <boost/python.hpp>

void a() {}

BOOST_PYTHON_MODULE(testbp)
{
  using namespace boost::python;

  def("a", a);
}
'''

def buildTestModule(paths):
    import os
    dir = os.path.join('tmp', 'testbp')
    if not os.path.exists(dir): os.makedirs(dir)
    
    src = os.path.join(dir, 'testbp.cc')
    open(src, 'w').write(testcode)
    # build
    so = os.path.join(dir, 'testbp.so')
    libsstr = ' '.join(['-L %s' % l for l in paths.clibs])
    from .Python import find as findpython
    pythonpaths = findpython()
    incstr = ' '.join(['-I %s' % i for i in paths.includes+pythonpaths.includes])
    cmd = 'g++ -shared -fpic -o %s -lboost_python %s %s %s' % (
        so, libsstr, incstr, src)
    if os.system(cmd):
        raise RuntimeError("%r failed" % cmd)
    save = os.path.abspath(os.curdir)
    os.chdir(dir)
    try:
        import testbp
    except ImportError as e:
        os.chdir(save)
        msg = 'Failed to build a simple boost python module. error: %s' % e
        raise RuntimeError(msg)
    else:
        os.chdir(save)
    return


def validate(paths):
    import os
    from .PathsFinder import assertExists
    assertExists('boost/python.hpp', paths.includes)
    assertExists('libboost_python.so*', paths.clibs)
    buildTestModule(paths)
    return


from .FromDefaultLocations import PathsFinder
fromDefaultLoc = PathsFinder(name, description, validator=validate)


from .FromEnvVariables import PathsFinder
fromEnvVars = PathsFinder(
    name, description,
    hints = "BOOSTPYTHON" ,
    validator = validate)


def find():
    toolset  = [fromDefaultLoc, fromEnvVars]
    from .search import search
    return search(toolset)


