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


name = 'pylons'
server = 'http://peak.telecommunity.com/dist'

def get( version = None, **kwds ):
    if version is None: version = "0.9.4"
    cmds = [
        'cd %s' % tarball_path,
        'wget %s/ez_setup.py' % server,
        ]

    if version == '0.9.4':
        cmds.append(
            'PYTHONPATH=%(pref)s/python:$PYTHONPATH python ez_setup.py --prefix=%(pref)s  --install-dir=%(pref)s/python Beaker==0.7.5' % {
            'pref': install_path,
            'version': version,
            }
            )
        pass # end if version == '0.9.4'

    cmds.append(
        'PYTHONPATH=%(pref)s/python:$PYTHONPATH python ez_setup.py --prefix=%(pref)s  --install-dir=%(pref)s/python Pylons==%(version)s' % {
        'pref': install_path,
        'version': version,
        }
        )

	
    def _(): 
        execute( ";".join(cmds) )
        from ..easy_install_support import import_site
        import_site()
        return
    return _
    


from . import tarball_path, install_path, execute


# version
__id__ = "$Id$"

# End of file 
