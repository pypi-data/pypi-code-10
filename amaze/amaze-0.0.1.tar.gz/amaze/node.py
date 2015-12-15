import re
from . import pattern

class Node:
    def __init__(self, fragment=None):
        self.children = []

        self.process_fragment(fragment)

    def process_fragment(self, fragment):
        pass

    def render(self, context):
        pass

    def render_children(self, context, children=None):
        if children is None:
            children = self.children

        def render_child(child):
            child_html = child.render(context)
            return '' if not child_html else str(child_html)

        return ''.join(map(lambda c: str(c.render(context)), children))

class Text(Node):
    def process_fragment(self, fragment):
        self.text = fragment

    def render(self, context):
        return self.text

class Variable(Node):
    def process_fragment(self, fragment):
        self.space = ''
        if fragment.startswith('::{'):
            self.name = fragment[3:-1]
        else:
            self.name = fragment[2:]
            self.space = fragment[-1]

    def render(self, context):
        return str(eval(self.name, context)) + self.space

class Each(Node):
    def process_fragment(self, fragment):
        variables, iterable = re.findall(pattern.each, fragment)[0]

        self.variables = list(v.strip() for v in variables.split(','))
        self.iterable = iterable

    def render(self, context):
        collection = eval(self.iterable, context)

        return ''.join(map(lambda it: self.render_children(dict(context, **dict(zip(self.variables, it)))), collection))

class With(Node):
    def process_fragment(self, fragment):
        stmt, name = re.findall(pattern.w, fragment)[0]

        self.stmt = stmt
        self.name = name

    def render(self, context):
        evaluated_statement = eval(self.stmt, context)

        return self.render_children(dict(context, **{self.name: evaluated_statement}))

class If(Node):
    def process_fragment(self, fragment):
        pass

    def render(self, context):
        return ''.join(map(lambda c: c.render(context) if c.evaluate_condition(context) else '', self.children))

class IfCondition(Node):
    def process_fragment(self, fragment):
        self.condition = re.findall(pattern.ifc, fragment)[0]

    def render(self, context):
        return self.render_children(context) 

    def evaluate_condition(self, context):
        return eval(self.condition, context)

class Else(IfCondition):
    def process_fragment(self, fragment):
        pass

    def evaluate_condition(self, context):
        return True

class Include(Node):
    def process_fragment(self, fragment):
        path, raw_context = re.findall(pattern.include, fragment)[0]

        self.path = path.strip('\'').replace('.', '/') + '.tmp'
        self.raw_context = raw_context

    def render(self, context):
        context = eval(self.raw_context, context)

        return self.template.render(context)

class Extend(Node):
    def process_fragment(self, fragment):
        self.path = fragment[9:-1].strip('\'').replace('.', '/') + '.tmp'

class SectionContainer:
    def __init__(self, section):
        self.section = section

    def render(self, context):
        return self.section.render(context)

    def set_section(self, section):
        section.set_parent(self.section)
        self.section = section

    def __getattr__(self, name):
        return getattr(self.section, name)
    
class Section(Node):
    def process_fragment(self, fragment):
        self.name = fragment.strip(':').split(' ')[-1]

    def set_parent(self, parent):
        self.parent = parent

    def render(self, context):
        return ''.join(map(lambda c: c.render(context), self.children))
