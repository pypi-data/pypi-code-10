from setuptools import setup, find_packages
setup(
    name = "hermes_pygments",
    version = "0.1",
    packages = ['hermes_pygments',],
    install_requires = ['Pygments'],
    author = "Scott Frazer",
    author_email = "scott.d.frazer@gmail.com",
    description = "Pygments for Hermes grammar files, abstract syntax trees, and parse trees",
    entry_points={
      'pygments.lexers': [
          'hgr = hermes_pygments.hermes_lexer:HermesGrammarFileLexer',
          'htree = hermes_pygments.hermes_lexer:HermesParseTreeLexer',
          'hast = hermes_pygments.hermes_lexer:HermesAstLexer'
        ]
    }
)
