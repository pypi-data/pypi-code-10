from markdown import markdown
from pkg_resources import resource_string



def zilch():
    return markdown("**Still** nothing!")

def nill():
	return(resource_string(__name__, 'data.txt'))
	# with open('data.txt') as f:
	# 	return f.read()