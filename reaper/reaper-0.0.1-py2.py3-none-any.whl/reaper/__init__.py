"""
Reaper

Deprecation warnings that turns automatically to Exception once your package version is bumped.
"""

__version__ = '0.0.1'

import warnings
import semver
import traitlets


class DeprecationException(DeprecationWarning):pass

class DeprecationReaper:
    """
    Decorator for a function to be deprecated and remove.

    The function will trigger a DeprecationWarning when called while the `versionspec` is not satisfied, 
    then raise once the version spec is satisfied.


    Deprecation warning Example:

        In [1]: from reaper import deprecate
        
        In [2]: @deprecate("IPython",">=5.0.0")
           ...: def function(value):
           ...:         return value
           ...:
        
        In [3]: function(1)
        DeprecationWarning: Support of `function` will end with IPython>=5.0.0
        Out[3]: 1

    Deprecation Error Example:
        
        In [4]: import IPython

        In [5]: IPython.__version__='5.0.0'

        In [6]: @deprecate("IPython",">=5.0.0")
           ...: def function(value):
           ...:         return value
           ...:
        ---------------------------------------------------------------------------
        DeprecationWarning                        Traceback (most recent call last)
        <ipython-input-6-52c92c195b7c> in <module>()
        ----> 1 @deprecate("IPython",">=5.0.0")
              2 def function(value):
              3         return value
              4

        DeprecationWarning: `function` is not supported on IPython>=5.0.0


    """
    
    def __init__(self, package, versionspec):

        # if something deprecated '>=4.1.0' we want it to raise during the 4.1.0-dev, and 4.1.0-rc, 
        # not just when we release 4.1.0, so remove any extra-tags.
        versionspec = versionspec.split('-')[0]

        current_version = traitlets.import_item(package+'.__version__')
        self.match =  semver.match(current_version, versionspec)
        self.package = package
        self.spec = versionspec


            

    def __call__(self, wrapped):
        data = {
            'name':wrapped.__qualname__,
            'p':self.package,
            's':self.spec,
        }
            
        if self.match:
            raise DeprecationException("`{name}` is not supported on {p}{s}".format(**data))
        else:
            def _wrap(*args, **kwargs):
                
                warnings.warn("Support of `{name}` will end with {p}{s}".format(**data), DeprecationWarning, stacklevel=2)
                return wrapped(*args, **kwargs)
            return _wrap
        

deprecate = DeprecationReaper
