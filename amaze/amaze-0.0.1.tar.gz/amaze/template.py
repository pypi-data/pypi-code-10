import re
import os
import ast

from . import node, token, config

default_context = {}

class Template:
    __slots__ = ['path', 'content', 'context', 'children', 'sections']

    def __init__(self, path):
        self.path = path
        self.children = []
        self.sections = {}

        with open(self.path, 'r') as fp:
            self.content = fp.read()

    def compile(self, fragments=None):
        root = self
        fragments = fragments or re.split(token.regex, self.content)

        depth = 0
        node_stack = [self]
        for fragment in fragments:
            if str.startswith(fragment, '::for'):
                n = node.Each(fragment)
                node_stack[-1].children.append(n)
                node_stack.append(n)
            elif fragment.startswith('::end'):
                while depth > 0:
                    node_stack.pop()
                    depth -= 1

                node_stack.pop()
            elif fragment.startswith('::with'):
                n = node.With(fragment)
                node_stack[-1].children.append(n)
                node_stack.append(n)
            elif fragment.startswith('::if'):
                depth = 1

                n = node.If('')
                ifc = node.IfCondition(fragment)
                n.children.append(ifc)

                node_stack[-1].children.append(n)
                node_stack.append(n)
                node_stack.append(ifc)
            elif fragment.startswith('::elif'):
                node_stack.pop()
                ifc = node.IfCondition(fragment)
                node_stack[-1].children.append(ifc)
                node_stack.append(ifc)
            elif fragment.startswith('::else'):
                node_stack.pop()
                ifc = node.Else(fragment)
                node_stack[-1].children.append(ifc)
                node_stack.append(ifc)
            elif fragment.startswith('::include'):
                n = node.Include(fragment)
                t = Template(os.path.join(config.base_path, n.path))
                t.compile()
                n.template = t

                node_stack[-1].children.append(n)
            elif fragment.startswith('::extend'):
                n = node.Extend(fragment)

                self.compile(re.split(token.regex, Template(config.base_path + n.path).content))
            elif fragment.startswith('::section'):
                n = node.Section(fragment)

                if n.name in self.sections:
                    sc = self.sections[n.name]
                    self.sections[n.name].set_section(n)
                else:
                    sc = node.SectionContainer(n)
                    self.sections[n.name] = sc
                    node_stack[-1].children.append(sc)

                node_stack.append(sc)
            elif fragment.startswith('::parent'):
                node_stack[-1].children.append(node_stack[-1].parent)
            elif fragment.startswith('::{'):
                node_stack[-1].children.append(node.Variable(fragment))
            elif fragment.startswith('::'):
                node_stack[-1].children.append(node.Variable(fragment))
            elif fragment.startswith('"""'):
                pass
            elif not fragment == '':
                node_stack[-1].children.append(node.Text(fragment))
    
    def impart(self, **kwargs):
        self.context.update(kwargs)

        return self

    def render(self, context=None):
        context = dict(default_context, **context)
        return ''.join(child.render(context) for child in self.children)

class TemplateContainer:
    def __init__(self, template):
        self.template = template
        self.context = {}

    def impart(self, **kwargs):
        self.context.update(kwargs)

        return self

    def __str__(self):
        return self.template.render(self.context)

    def render(self):
        return str(self)
