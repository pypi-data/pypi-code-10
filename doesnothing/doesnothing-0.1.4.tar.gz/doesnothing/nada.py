from markdown import markdown

def zilch():
    return markdown("**Still** nothing!")

def nill():
	with open('data.txt') as f:
		return f.read()