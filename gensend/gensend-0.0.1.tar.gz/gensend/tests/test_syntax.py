from . import TestingHelper


class TestTokenizer(TestingHelper):

    def test_literal_tokens(self):
        patterns = [
            ['literal ":"', 'literal ":"'],
            ['literal "\:"', 'literal ":"'],
            ['literal ","', 'literal ","'],
            ['literal "\,"', 'literal ","'],
            ['literal "}"', 'literal "}"'],
            ['literal "\}"', 'literal "}"'],
            ['literal "\\\\"', 'literal "\\"'],
            ['literal "%"', 'literal "%"'],
            ['literal "{"', 'literal "{"'],
            ['literal "\\%{"', 'literal "%{"'],
        ]
        self.assert_patterns(patterns)

    def test_escaping_edge(self):
        patterns = [
            ['is backslash "\\"', 'is backslash "\\"'],
            ['is backslash "\\\\}" followed by close tok', 'is backslash "\\}" followed by close tok'],
            ['is backslash "\\\\%{int}" followed by valid open tok',
                'is backslash "\\4865782901354085937" followed by valid open tok'],
            ['slash city "\\\\\\%{int}"', 'slash city "\\%{int}"'],
        ]
        self.assert_patterns(patterns)


class TestParser(TestingHelper):

    def test_nesting(self):
        patterns = [
            ['depth 0 = %{FIRST:1,2,3}', 'depth 0 = 1'],
            ['depth 1 = %{FIRST:%{FIRST:4,5,6},1,2,3}', 'depth 1 = 4'],
            ['depth 2 = %{FIRST:%{FIRST:%{FIRST:%{FIRST:7,8,9},2,3},4,5,6},1,2,3}', 'depth 2 = 7'],
            ['depth 3 = %{FIRST:%{FIRST:%{FIRST:%{FIRST:%{FIRST:10,11,12},8,9},2,3},4,5,6},1,2,3}', 'depth 3 = 10'],
        ]
        self.assert_patterns(patterns)
