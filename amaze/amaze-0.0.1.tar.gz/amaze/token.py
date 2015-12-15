import re

comment = '"""'
var_start = '::'
varg_start = '::{'
varg_end = '}'
block_start = '::'
block_end = ':'
end = '::end'

regex = re.compile(r"(%s.*?%s|%s[A-z]+?\(.*?\)|%s.*?%s|%s.*?%s|%s\s|%s.*?\s)" % (
    comment, comment,
    var_start,
    varg_start, varg_end,
    block_start, block_end,
    end,
    var_start
))
