#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from ..paths.InstallationNotFound import InstallationNotFound


def render_file( path, dependencies,
                 export_root, build_root, merlin_dir,
                 target = 'shared,opt', 
                 customization_path = None):
    """
    path: path of the .tools file
    dependencies: dependencies of the project
    export_root: path of export root
    build_root: path to build
    merlin_dir: path to merlin 
    target: build target
    customization_path: path of the .tools-customization, if necessary
    """
    f = Factory(
        export_root, build_root, merlin_dir, target, 
        customization_path = customization_path)
    lines = f( dependencies )
    open(path, 'w').write( '\n'.join( lines ) )
    return


class DependencyMissing(Exception):

    def __init__(self, packagename, packageid=None,
                 errormessage=None, suggestion=None):
        self.packagename = packagename
        self.packageid = packageid or packagename
        self.errormessage = errormessage
        self.suggestion = suggestion
        return
    
    pass


class Factory:

    def __init__(self,
                 export_root,
                 build_root,
                 merlin_dir,
                 target = 'shared,opt',
                 customization_path = None,
                 ):
        self.target = target
        self.export_root = export_root
        self.build_root = build_root
        self.merlin_dir = merlin_dir
        self.customization_path = customization_path
        return


    def __call__(self, dependencies = [ 'Python' ]):
        import os
        merlin_dir = self.merlin_dir
        build_root = self.build_root
        export_root = self.export_root
        
        from . import dottools
        header = dottools.render_header(
            self.target, export_root, build_root, merlin_dir )

        lines = header
        for dep in dependencies:
            try:
                print("rendering .tools codes for %r ..." % dep)
                lines += dottools.render_dependency( dep )
            except InstallationNotFound as err:
                pkgname = err.packagename or dep
                pkgid = err.packageid or dep
                msg = err.errormessage
                if not msg:
                    import traceback
                    msg = traceback.format_exc()
                raise DependencyMissing(
                    pkgname,
                    packageid = pkgid,
                    errormessage = msg,
                    suggestion = err.possible_solution)
            continue
        
        # .tools-customized
        customization_path = self.customization_path
        if customization_path:
            if not os.path.exists(customization_path):
                open(customization_path, 'w').write('')
            lines.append(". %s" % customization_path)
            
        return lines
        
    pass # end of Factory


# version
__id__ = "$Id$"

# End of file 
