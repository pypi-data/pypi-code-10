#!/bin/python2

from sys import argv
from astparser import AstParser
from graphviz import Digraph

identifiers = []

def handle_node(node, graph, parent=None):
    if node.id:
        name = node.id
    else:
        name = str(id(node.label))
    graph.node(name, node.label, shape="rect", style="rounded")
    if parent:
        graph.edge(parent, name)
    for child in node.children:
        handle_node(child, graph, parent=name)

def handle_edges(edges, graph):
    for edge in edges:
		graph.edge(edge.src, edge.dst, constraint="False", style="dashed")

def visualize(content, target):
    parser = AstParser()
    ast = parser.parse(content, rule_name='ast')
    graph = Digraph(comment=argv[1])
    handle_node(ast, graph)
    handle_edges(ast.edges, graph)
    graph.render(target, view=False)

def main():
    if len(argv) > 1:
        target = "output.gv"
        if len(argv) > 2:
            target = argv[2]
        with open(argv[1], "r") as f:
            content = f.read()
            visualize(content, target)
    else:
        print "No input file specified."

if __name__ == "__main__":
    main()
