"""
handle paths for cctbx package
"""

name = "cctbx"
description = 'crystallography tool box'


from .FromEnvVariables import PathsFinder as base_FromEnvVars


class FromEnvVars(base_FromEnvVars):

    def extract(self):
        """
        extract my paths from system environment variables
        """
        variableName = self._hintsToFindPaths
        derivedFrom  = self._derivedFrom
##         from envUtils import set_usingExec
##         #use Mike's infect utils to search for cctbx root
##         set_usingExec( variableName, "cctbx.python", "cctbx_build/bin")
        
        
        from .envUtils import getEnv
        from os.path import join

        self.variableName = variableName
        
        base_desc = self.description
        desc_str = 'path to %s of ' + base_desc
        if derivedFrom is None:
            root =  getEnv( '%s' % variableName,
                            None,
                            desc_str % " root")
            pass
        else:
            root =  getEnv( '%s' % variableName,
                            self.getPaths(derivedFrom).root,
                            desc_str % " root")
            pass
            

        source = getEnv('CCTBX_SOURCES', join(root, 'cctbx_sources'),
                        'source tree of cctbx')
        build = getEnv('CCTBX_BUILD', join(root, 'cctbx_build'),
                       'build tree of cctbx')
        clib = getEnv('CCTBX_LIBDIR', join(build,'lib'),
                     'library directory of cctbx')
        #older version of cctbx also use cctbx/cctbx_build/libtbx
        clib_older = getEnv('CCTBX_LIBDIR_OLD', join(build,'libtbx'),
                            'library directory of older version of cctbx')
        
        default_boost_inc = join(source, 'boost')
        boost_inc = getEnv('BOOST_PYTHON_INCDIR', default_boost_inc,
                           'boost python headers')
        cctbx_inc = join(source, 'cctbx', 'include')
        scitbx_inc = join(source, 'scitbx', 'include')
        cctbx_build_inc = join(build, 'include')

        includes= [
            cctbx_build_inc,
            boost_inc,
            cctbx_inc,
            scitbx_inc,
            ]

        modules = [
            join(source,'boost_adaptbx'),
            join(source,'scitbx'),
            join(source,'cctbx'),
            join(source,'iotbx'),
            join(source,'libtbx'),
            build]

        from .Paths import Paths
        return Paths(
            name,
            root = root,
            includes= includes,
            clibs= [clib, clib_older],
            origin = self.mechanism,
            description = self.description,
            modules= modules)
        

def find():
    from .search import search

    fromEnvVars = FromEnvVars( name, description, hints = "CCTBX_ROOT" )

    paths = search( [fromEnvVars] )
    return paths
