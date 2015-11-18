import re

from pygments.lexer import RegexLexer, include, bygroups, using, this
from pygments.token import Error, Punctuation, Text, Comment, Operator, Keyword, Name, String, Number


class PseudocodeLexer(RegexLexer):
    '''
    A Pseudo code (fr) lexer
    '''
    name = 'Pseudocode'
    aliases = ['pseudocode', 'pseudo', 'algorithm', 'algo']
    filenames = ['*.algo', '*.pseudocode']
    mimetypes = []
    flags = re.IGNORECASE

    # Data Types: INTEGER, REAL, COMPLEX, LOGICAL, CHARACTER  and DOUBLE PRECISION
    # Operators: **, *, +, -, /, <, >, <=, >=, ==, /=
    # Logical (?): NOT, AND, OR, EQV, NEQV
    
    # Builtins: http://gcc.gnu.org/onlinedocs/gcc-3.4.6/g77/Table-of-Intrinsic-Functions.html 
     
    tokens = {
        'root': [
                 (r'\/\*.*\*\/', Comment),
                 include('strings'),
                 include('core'),
                 (r'[a-z][a-z0-9_]*', Name.Variable),
                 include('nums'),
                 (r'[\s]+', Text)
        ],
        'core':[ # Statements
                 (r'\b(debut|début|fin|si|alors|sinon|fin_si|tant_que|tantque|fin_tantque|faire|répéter'
                  r'repeter|type|structure|fin_structure|fonction|procédure|procedure|retourner|renvoyer'
                  r')\s*\b', Keyword),

                 # Data Types
                 (r'\b(entier|chaine|chaîne|réel|reel|caractère|caractere|booléen|booleen)\s*\b', 
                  Keyword.Type),
                  
                 # Operators
                 (r'(\*|\+|-|\/|<|>|<=|>=|=|<>|\\\\|mod|<-|←|≤|≥|≠|÷|×|:)',
                  Operator),
                  
                 (r'(\(|\)|\,|\;)',
                  Punctuation),
                  
                 (r'(:)',
                  Keyword.Declaration),

                  # Intrinsics
                 (r'\b(sqrt|pow|cos|sin|tan|arccos|arcsin|arctan|arctan2|lire|ecrire|écrire|'
                  r'exp|ln|log'
                  r')\s*\b', Name.Builtin)
                ],

        'strings': [
                 (r'"([^"])*"', String.Double),
                 (r"'([^'])*'", String.Single),
                ],

        'nums': [
                 (r'\d+(?![.Ee])', Number.Integer),
                 (r'[+-]?\d*\.\d+([eE][-+]?\d+)?', Number.Float),
                 (r'[+-]?\d+\.\d*([eE][-+]?\d+)?', Number.Float)
                ],
        }
