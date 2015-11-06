from .providers import ProviderList, ProviderAccessor


class Generator(ProviderAccessor):
    def __init__(self, provider_list=None):
        self.tokenizer = Tokenizer()
        self.parser = Parser()
        self.provider_list = ProviderList()
        self.patterns = []

        if provider_list:
            self.add_providers(provider_list)

    def compile(self, pattern, provider_list=None):
        if provider_list is None:
            provider_list = self.provider_list

        generatable = Generatable(self.provider_list, pattern)
        tokens = self.tokenizer.tokenize(pattern)
        ctx = ParserCtx(generatable, tokens)
        self.parser.parse(ctx)

        return generatable

    def run(self, pattern):
        return self.compile(pattern)()

    def generate(self, patterns, rounds=1):
        for i in range(rounds):
            for pattern in patterns:
                yield self.compile(pattern)


class Printable(object):
    def __str__(self):
        space = "  "
        height = self.height + 1
        label = self.__class__.__name__
        spacer = space * height
        out = spacer

        if 0 == height:
            label += "(Root)"
        else:
            label += "(" + str(height) + ")"
        out += label

        if len(self.payload):
            out += "\n" + spacer + (space * 2) + "-> " + str(self.payload)

        out += "\n"
        for child in self.children:
            out += str(child)
        return out

    def __repr__(self):
        return str(self.__class__.__name__) + "(" + str(self.__dict__) \
            .replace("'", '').replace("{", '').replace("}", ', ').rstrip(', ') + ")"


class Token(Printable):
    TOK_STR = 'TOK_STR'  # '*'
    TOK_OPEN = 'TOK_OPEN'  # '%{'
    TOK_CLOSE = 'TOK_CLOSE'  # '}'
    TOK_SEP = 'TOK_SEP'  # ':'
    TOK_ARG_SEP = 'TOK_ARG_SEP'  # ','

    def __init__(self, tok, val, pos):
        self.tok = tok
        self.val = val
        self.pos = pos


class Tokenizer(Printable):
    def __init__(self):
        self.buf = ''
        self.end = 0
        self.pos = 0

    def at(self, pos):
        if (pos >= self.end) or pos < 0:
            return None
        return self.buf[pos]

    @property
    def lo(self):
        return self.at(self.pos)

    @property
    def lb(self):
        return self.at(self.pos-1)

    @property
    def la(self):
        return self.at(self.pos+1)

    def scan(self, pattern):
        self.pos = 0
        self.buf = pattern
        self.end = len(pattern)

        while 1:
            token = self.tok()
            if not token:
                break
            yield token

    def tok(self):
        token = None

        if '\\' == self.lo and self.la in ('%', ',', ':', '{', '}', '\\'):
            self.pos += 1
            token = Token(Token.TOK_STR, self.lo, self.pos)
        elif '%' == self.lo and '{' == self.la:
            self.pos += 1
            token = Token(Token.TOK_OPEN, None, self.pos)
        elif '}' == self.lo:
            token = Token(Token.TOK_CLOSE, None, self.pos)
        elif ':' == self.lo:
            token = Token(Token.TOK_SEP, None, self.pos)
        elif ',' == self.lo:
            token = Token(Token.TOK_ARG_SEP, None, self.pos)
        elif self.lo:
            token = Token(Token.TOK_STR, self.lo, self.pos)
        self.pos += 1
        return token

    def tokenize(self, pattern):
        return list(self.scan(pattern))


class Node(Printable):
    def __call__(self):
        return str(self.execute())

    def __init__(self, payload=None):
        if payload is None:
            payload = ''
        self.payload = payload
        self.parent = None
        self.children = []

    @property
    def top(self):
        parent = self

        while parent.parent:
            parent = parent.parent
        return parent

    @property
    def height(self):
        height = -1
        parent = self

        while parent:
            height += 1
            parent = parent.parent
        return height

    def add(self, node):
        node.parent = self
        self.children.append(node)

    def execute(self):
        return self.payload


class StringNode(Node):
    def execute(self):
        result = self.payload

        for child in self.children:
            result += child()
        return result


class ExprNode(Node):
    def execute(self):
        if not len(self.payload):
            return ''
        expr = self.payload
        expr_args = []

        for child in self.children:
            expr_args.append(child())
        return self.top.call_provider(expr, expr_args)


class Generatable(StringNode, ProviderAccessor, Printable):
    def __init__(self, provider_list, source):
        Node.__init__(self)
        self.provider_list = provider_list
        self.source = source


class Parser(Printable):
    def __init__(self):
        self.token_call_map = {
            Token.TOK_OPEN: 'do_tok_open',
            Token.TOK_SEP: 'do_tok_sep',
            Token.TOK_ARG_SEP: 'do_tok_arg_sep',
            Token.TOK_CLOSE: 'do_tok_close',
            Token.TOK_STR: 'do_tok_str',
        }

    def parse(self, ctx):
        self.begin(ctx)
        self.walk(ctx)
        self.end(ctx)

    def begin(self, ctx):
        ctx.begin()

    def walk(self, ctx):
        for token in ctx.tokens:
            if token.val:
                getattr(ctx, self.token_call_map[token.tok])(token.val)
            else:
                getattr(ctx, self.token_call_map[token.tok])()

    def end(self, ctx):
        ctx.end()


class ParserCtx(Printable):
    STATE_EXIT = 'STATE_EXIT'
    STATE_IDLE = 'STATE_IDLE'
    STATE_STR = 'STATE_STR'
    STATE_EXPR = 'STATE_EXPR'
    STATE_EXPR_ARG = 'STATE_EXPR_ARG'

    def __init__(self, generatable, tokens):
        self.generatable = generatable
        self.tokens = tokens
        self.stack = [generatable]
        self.state = [ParserCtx.STATE_IDLE]

    @property
    def stack_top(self):
        return self.stack[-1] if len(self.stack) else None

    @property
    def state_top(self):
        return self.state[-1] if len(self.state) else ParserCtx.STATE_EXIT

    def begin(self):
        self.enter(ParserCtx.STATE_STR)

    def end(self):
        while 1:
            popped = self.stack.pop()
            if not self.stack_top:
                break
            self.stack_top.add(popped)

    def enter(self, to_state):
        old_state = self.state_top
        cur_state = to_state
        cur_node = None

        assert ParserCtx.STATE_IDLE != to_state, 'unable to transition to idle'
        assert cur_state != old_state, 'unable to transition to same state'

        if ParserCtx.STATE_STR == old_state:
            self.exit()
        if ParserCtx.STATE_STR == cur_state:
            cur_node = StringNode()
        elif ParserCtx.STATE_EXPR == cur_state:
            cur_node = ExprNode()
        elif ParserCtx.STATE_EXPR_ARG == cur_state:
            cur_node = StringNode()

        assert not (cur_node is None), 'unable to derive a new node from state transition'

        self.state.append(to_state)
        self.stack.append(cur_node)

    def exit(self):
        self.state.pop()
        old_node = self.stack.pop()
        self.stack_top.add(old_node)

    def do_tok_str(self, s):
        if ParserCtx.STATE_IDLE == self.state_top:
            self.enter(ParserCtx.STATE_STR)
        if len(self.stack_top.children):
            self.stack_top.children.append(StringNode(s))
        else:
            self.stack_top.payload += s

    def do_tok_open(self):
        self.enter(ParserCtx.STATE_EXPR)

    def do_tok_sep(self):
        if ParserCtx.STATE_EXPR == self.state_top:
            self.enter(ParserCtx.STATE_EXPR_ARG)
        else:
            self.do_tok_str(':')

    def do_tok_arg_sep(self):
        if ParserCtx.STATE_EXPR_ARG == self.state_top:
            self.exit()
            self.enter(ParserCtx.STATE_EXPR_ARG)
        else:
            self.do_tok_str(',')

    def do_tok_close(self):
        if self.state_top in (ParserCtx.STATE_STR, ParserCtx.STATE_IDLE):
            self.do_tok_str('}')
        else:
            if ParserCtx.STATE_EXPR_ARG == self.state_top:
                self.exit()
            self.exit()
