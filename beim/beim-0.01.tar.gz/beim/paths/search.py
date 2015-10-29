from beim import logger
from ..misc._formatstr import indent
from .InstallationNotFound import InstallationNotFound
from .PathsFinder import ValidationError
import traceback
from functools import reduce
            

def search( pathsFinders=[] ):
    """search for package with packageName and description 
    """
    if not pathsFinders:
        return
    
    errorMsgs = []
    for pathsFinder in pathsFinders:
        try:
            paths = pathsFinder.extract()
            return paths
        except ValidationError as msg:
            msg = indent(str(msg), '  ')
            errorMsgs.append( '* Unable to validate paths for package %r obtained from mechanism %r\n  -> The reason of validation failure is \n\n%s\n\n' %(pathsFinder.name, pathsFinder.mechanism, msg) )
            logger.debug(traceback.format_exc())
        except Exception as msg:
            msg = indent(str(msg), '  ')
            errorMsgs.append( '* Unable to find package %s using mechanism %r.\n -> The reason of failing is \n\n%s\n\n' %(pathsFinder.name, pathsFinder.mechanism, msg) )
            logger.debug(traceback.format_exc())
        continue
    
    #nothing useful found. raise error
    from operator import add
    raise InstallationNotFound(
        pathsFinders[0].name,
        reduce(add, errorMsgs)
        )


