from aliasfile.utils import escape_argument


class Test_escape_argument:

    def test_only_letters_will_not_be_wrapped(self):
        assert escape_argument('foobar') == 'foobar'

    def test_string_with_space_will_be_wrapped_in_quotes(self):
        assert escape_argument('foo bar') == '"foo bar"'

    def test_newline_is_escaped(self):
        assert escape_argument('foo\nbar') == '"foo\\nbar"'

    def test_backslash_is_escaped(self):
        assert escape_argument('foo\\bar') == '"foo\\\\bar"'
