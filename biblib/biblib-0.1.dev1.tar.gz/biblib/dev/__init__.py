
__license__ = "MIT"
__docformat__ = 'reStructuredText'
__version__   = '0.1.dev1'
__revision__  = filter(str.isdigit, "$Revision: 84 $")


from ._parser import parse_data
from ._latexenc import (latex_to_string, string_to_latex)
from ._doilib  import (doi2bibtex, DOIError)


__all__ = ('parse_data', 'latex_to_string', 'string_to_latex', 'doi2bibtex', 'DOIError')

