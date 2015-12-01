from pygments.lexer import this, include, bygroups, using, RegexLexer, ExtendedRegexLexer
from pygments.lexers.python import PythonLexer
from pygments.lexers.c_cpp import CLexer
from pygments.lexers.javascript import JavascriptLexer
from pygments.lexers.jvm import JavaLexer
from pygments.token import Token
import re
import sys

class HermesParseTreeLexer(RegexLexer):
  name = 'Hermes Parse Tree Lexer'
  aliases = ['htree']
  filenames = ['*.htree']
  mimetypes = []
  flags = re.DOTALL

  tokens = {
      'whitespace': [
        (r'\s+', Token.Text),
      ],

      'parsetree': [
        (r'(\()([a-zA-Z0-9_]+)(:)', bygroups(Token.Punctuation, Token.Name.Class, Token.Punctuation), 'children')
      ],

      'token': [
        (r'(<)([a-zA-Z0-9_]+:\d+:\d+ [a-zA-Z0-9_]+ "[^"]*")(>)', bygroups(Token.Punctuation, Token.Number.Integer, Token.Punctuation))
      ],

      'children': [
        include('whitespace'),
        include('parsetree'),
        include('token'),
        (r',', Token.Punctuation),
        (r'\)', Token.Punctuation, '#pop')
      ],

      'root': [
        include('whitespace'),
        include('parsetree')
      ]
  }

class HermesAstLexer(ExtendedRegexLexer):
  name = 'Hermes Abstract Syntax Tree Lexer'
  aliases = ['hast']
  filenames = ['*.hast']
  mimetypes = []
  flags = re.DOTALL

  def attr_terminator(lexer, match, ctx):
      ctx.stack = ctx.stack[:-1] # Pop stack
      ctx.pos = match.start() # Leave token to process
      yield match.start(), Token.Punctuation, ''

  tokens = {
      'whitespace': [
        (r'\s+', Token.Text),
      ],

      'ast': [
        (r'(\()([a-zA-Z_]+)(:)', bygroups(Token.Punctuation, Token.Name.Class, Token.Punctuation), 'ast_attrs')
      ],

      'attr': [
        (r'([a-zA-Z_]+)(=)', bygroups(Token.Name.Variable, Token.Punctuation), 'ast_attr')
      ],

      'token': [
        (r'(<)([a-zA-Z0-9_]+:\d+:\d+ [a-zA-Z0-9_]+ "[^"]*")(>)', bygroups(Token.Punctuation, Token.Number.Integer, Token.Punctuation))
      ],

      'ast_attr_list': [
        include('whitespace'),
        include('ast'),
        include('attr'),
        include('token'),
        (r',', Token.Punctuation),
        (r'\[', Token.Punctuation, '#push'),
        (r'[\)\]]', Token.Punctuation, '#pop')
      ],

      'ast_attr': [
        include('whitespace'),
        include('ast'),
        include('token'),
        (r'None', Token.Integer),
        (r'\[', Token.Punctuation, 'ast_attr_list'),
        (r'(,|\)|\])', attr_terminator)
      ],

      'ast_attrs': [
        include('whitespace'),
        include('ast'),
        include('attr'),
        (r',', Token.Punctuation),
        (r'[\)\]]', Token.Punctuation, '#pop'),
      ],

      'root': [
        include('whitespace'),
        (r'\[', Token.Punctuation, 'ast_attr_list'),
        include('ast')
      ]
  }

class HermesGrammarFileLexer(ExtendedRegexLexer):
  name = 'Hermes Grammar File Lexer'
  aliases = ['hgr']
  filenames = ['*.hgr']
  mimetypes = []
  flags = re.DOTALL
  language = None
  blah = None

  Terminal = Token.Literal
  NonTerminal = Token.Name.Variable
  Macro = Token.Keyword.Reserved
  Regex = Token.String.Regex
  Section = Token.Keyword.Declaration
  SectionType = Token.Keyword.Type
  AstName = Token.Name.Function
  AstKey = Token.Name.Attribute
  ProductionRef = Token.Name.Function
  NewBindingPower = Token.Operator
  KeepBindingPower = Token.Operator
  Associativity = Token.Operator.Word
  ExpressionDivider = Token.Name.Function

  def newline_terminator(lexer, match, ctx):
      ctx.stack = ctx.stack[:-1] # Pop stack
      ctx.pos = match.start() # Leave \n to process
      yield match.start(), Token.Text, ''

  def lexer_decl(lexer, match, ctx):
      groups = match.groups()
      def offset(group): return match.start() + sum([len(groups[x]) for x in range(group)])
      lexer.language = groups[4]
      lexer.blah = PythonLexer
      ctx.stack.append('lexer') # Push 'lexer' state
      ctx.pos = match.end()
      return [
        (offset(0), HermesGrammarFileLexer.Section, groups[0]),
        (offset(1), Token.Text, groups[1]),
        (offset(2), Token.Punctuation, groups[2]),
        (offset(3), Token.Text, groups[3]),
        (offset(4), HermesGrammarFileLexer.SectionType, groups[4]),
        (offset(5), Token.Text, groups[5]),
        (offset(6), Token.Punctuation, groups[6]),
        (offset(7), Token.Text, groups[7]),
        (offset(8), Token.Punctuation, groups[8])
      ]

  def language_lex(lexer, match, ctx):
    yield match.start(), Token.Text, match.group(0)
    ctx.pos = match.end()
    ctx.stack.append(lexer.language + '_code')

  tokens = {
      'whitespace': [
        (r'\s+', Token.Text)
      ],

      'spacetab': [
        (r'[\ \t]+', Token.Text)
      ],

      'parser': [
        include('whitespace'),
        (r'}', Token.Punctuation, '#pop')
      ],

      'terminal': [
        (r':[a-zA-Z0-9_]+', Terminal),
      ],

      'nonterminal': [
        (r'\$[a-zA-Z0-9_]+', NonTerminal),
      ],

      'lexer_func_body': [
        include('whitespace'),
        include('terminal'),
        (r'\(', Token.Punctuation),
        (r',', Token.Punctuation),
        (r'\)', Token.Punctuation, '#pop'),
      ],

      'regex_options': [
        include('whitespace'),
        (r'[a-zA-Z0-9_\.]+', Token.Name.Variable),
        (r',', Token.Punctuation),
        (r'}', Token.Punctuation, '#pop')
      ],

      'end_code': [(r'</code>', Token.Text, '#pop')],

      'python_code': [
        include('end_code'),
        (r'(.*?)(?=</code>)', using(PythonLexer)),
      ],

      'c_code': [
        include('end_code'),
        (r'(.*?)(?=</code>)', using(CLexer)),
      ],

      'javascript_code': [
        include('end_code'),
        (r'(.*?)(?=</code>)', using(JavascriptLexer)),
      ],

      'java_code': [
        include('end_code'),
        (r'(.*?)(?=</code>)', using(JavaLexer)),
      ],

      'lexer': [
        include('whitespace'),
        include('terminal'),
        (r'<code>', language_lex),
        (r'r\'(\\\'|[^\'])*\'', Regex),
        (r'"(\\\"|[^\"])*"', Regex),
        (r'->', Token.Punctuation),
        (r'null', Token.Keyword.Type),
        (r'(mode)(<)([a-zA-Z0-9_]+)(>)(\s*)({)', bygroups(Section, Token.Punctuation, SectionType, Token.Punctuation, Token.Text, Token.Punctuation), 'lexer'),
        (r'[a-zA-Z][a-zA-Z0-9_]+', Token.Name.Function, 'lexer_func_body'),
        (r'{', Token.Punctuation, 'regex_options'),
        (r'}', Token.Punctuation, '#pop')
      ],

      'macro': [
        include('spacetab'),
        include('nonterminal'),
        include('terminal'),
        (r'[0-9]+', Token.Number.Integer),
        (r',', Token.Punctuation),
        (r'\)', Token.Punctuation, '#pop')
      ],

      'ast_spec': [
        include('spacetab'),
        include('production_ref'),
        (r'=', Token.Punctuation),
        (r',', Token.Punctuation),
        (r'[a-zA-Z0-9_]+', AstKey),
        (r'\)', Token.Punctuation, '#pop')
      ],

      'ast_transformation': [
        include('spacetab'),
        (r'\n', newline_terminator),
        include('production_ref'),
        (r'([a-zA-Z0-9_]+)(\s*)(\()', bygroups(AstName, Token.Text, Token.Punctuation), 'ast_spec'),
      ],

      'production_ref': [
        (r'\$[0-9\$]+', ProductionRef),
      ],

      'expression_parser': [
        include('whitespace'),
        include('nonterminal'),
        (r'(\()(\s*)(\*)(\s*)(:)(\s*)(left|right|unary)(\s*)(\))', bygroups(Token.Punctuation, Token.Text, NewBindingPower, Token.Text, Token.Punctuation, Token.Text, Associativity, Token.Text, Token.Punctuation)),
        (r'(\()(\s*)(-)(\s*)(:)(\s*)(left|right|unary)(\s*)(\))', bygroups(Token.Punctuation, Token.Text, KeepBindingPower, Token.Text, Token.Punctuation, Token.Text, Associativity, Token.Text, Token.Punctuation)),
        (r'=', Token.Punctuation, 'production'),
        (r'}', Token.Punctuation, '#pop')
      ],

      'production': [
        (r'\n', newline_terminator),
        (r'[\ \t]+', Token.Text),
        (r'(parser)(<)(expression)(>)(\s*)({)', bygroups(Section, Token.Punctuation, SectionType, Token.Punctuation, Token.Text, Token.Punctuation), 'expression_parser'),
        include('terminal'),
        include('nonterminal'),
        (r'(list|otlist|tlist|mlist|optional)(\s*)(\()', bygroups(Macro, Token.Text, Token.Punctuation), 'macro'),
        (r'\|', Token.Punctuation),
        (r'->', Token.Punctuation, 'ast_transformation'),
        (r'<=>', ExpressionDivider),
      ],

      'parser': [
        include('whitespace'),
        include('nonterminal'),
        (r'=', Token.Punctuation, 'production'),
        (r'}', Token.Punctuation, '#pop')
      ],

      'grammar': [
        include('whitespace'),
        (r'(lexer)(\s*)(<)(\s*)([a-zA-Z]+)(\s*)(>)(\s*)({)', lexer_decl),
        (r'(parser)(<)(ll1)(>)(\s*)({)', bygroups(Section, Token.Punctuation, SectionType, Token.Punctuation, Token.Text, Token.Punctuation), 'parser'),
        (r'}', Token.Punctuation, '#pop')
      ],

      'root': [
        include('whitespace'),
        (r'grammar', Section),
        (r'{', Token.Punctuation, 'grammar'),

        # These are to allow processing of rules, nonterminals, and terminals all by themselves
        include('nonterminal'),
        include('terminal'),
        (r'=', Token.Punctuation, 'production'),
      ],

  }

