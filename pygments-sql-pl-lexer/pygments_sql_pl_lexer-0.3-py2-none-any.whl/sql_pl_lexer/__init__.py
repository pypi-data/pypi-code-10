# -*- coding: utf-8 -*-

from pygments.lexers.sql import SqlLexer
from pygments.token import Name, Keyword

class SqlPlLexer(SqlLexer):
    name = 'SQL Procedural Language (SQL PL)'
    aliases = ['sqlpl']

    EXTRA_KEYWORDS = ['MODULE', 'DOUBLE', 'ASIN', 'SIGNAL', 'IF']

    def get_tokens_unprocessed(self, text):
        for index, token, value in SqlLexer.get_tokens_unprocessed(self, text):
            if token in Name and value in self.EXTRA_KEYWORDS:
                yield index, Keyword, value
            else:
                yield index, token, value
