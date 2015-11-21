from collections import OrderedDict


def render_attrs(attrs, xhtml=False, exclude=[]):
    result = []
    is_true = ['true']
    is_false = ['false', 'none', 'null']

    for key, value in attrs.items():
        if key.startswith('_'): key = key[1:]
        key = key.replace('_', '-')

        if key not in exclude:
            if type(value) == bool:
                if value:
                    if xhtml:
                        result.append('%s="%s"' % (key, key))
                    else:
                        result.append(key)
            else:
                if type(value) !=  str:
                    value = str(value)

                if value.lower() in is_true:
                    if xhtml:
                        result.append('%s="%s"' % (key, key))
                    else:
                        result.append(key)

                if value.lower() not in is_false:
                    result.append('%s="%s"' % (key, value))

    return ' '.join(result)


def render_tag(tag, content=None, _single=False, _xhtml=False, **attrs):
    attrs = render_attrs(attrs, xhtml=_xhtml)
    html = '<' + tag

    if attrs:
        html += ' ' + attrs

    html += ' />' if _xhtml and (not content or not _single) else '>'

    if content:
        html += content

    if content or not _single:
        html += '</%s>' % tag

    return html


def parse_attrs(atts_str, exclude=[]):
    attrs = OrderedDict()

    in_value = False
    attr_name = ''
    buffer = ''

    def fix_attr_name(attr_name):
        return attr_name.replace('-', '_')

    for char in atts_str:
        if char == ' ' and not in_value:
            if buffer:
                attrs[fix_attr_name(buffer)] = True
                buffer = ''
            continue

        if char == '=':
            if not in_value:
                attr_name = buffer
                buffer = ''
            continue

        if char == '"':
            if in_value:
                attrs[fix_attr_name(attr_name)] = buffer
                in_value = False
                buffer = ''
            else:
                in_value = True
            continue

        buffer += char

    if buffer and not in_value:
        attrs[fix_attr_name(buffer)] = True

    return attrs


SINGLE_TAGS = ('input', 'link', 'img', 'br')

class HtmlTags:
    def __init__(self, xhtml=False):
        self.tags_preset = {tag: {'_single': True} for tag in SINGLE_TAGS}
        self.xhtml = xhtml

    def __getattr__(self, tag_name):
        def wrapper(content=None, **attrs):
            final_attrs = {}
            if tag_name in self.tags_preset:
                final_attrs.update(self.tags_preset[tag_name])
            final_attrs.update(attrs)
            return render_tag(tag_name, content, _xhtml=self.xhtml, **final_attrs)
        return wrapper


tags = HtmlTags()
