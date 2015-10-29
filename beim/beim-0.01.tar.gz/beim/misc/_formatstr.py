def indent(s, tag):
    lines = s.splitlines()
    lines = ['%s%s' % (tag, l) for l in lines]
    return '\n'.join(lines)
