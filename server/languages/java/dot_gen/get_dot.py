from antlr4 import CommonTokenStream, InputStream

from java.dot_gen.TreeLexer import TreeLexer
from java.dot_gen.TreeParser import TreeParser


def evaluateTree(string):
    if not string[-1] == '\n':
        string += "\n"
    lex = TreeLexer(InputStream(string))
    tokens = CommonTokenStream(lex)
    parser = TreeParser(tokens)
    parser.tree_def()
    return parser.node_list, parser.connections


def get_dot(tree):
    data = "digraph g {"
    data += "\nnode [color=lightblue2, style=filled];"

    # tree = tree.replace("/", "\/")
    # Now we go parsing. Evaluate() returns us a list of nodes and
    # a list of connections.
    nodes, connections = evaluateTree(tree)

    # print nodes
    for (node, label) in nodes:
        data += "\n{} [ label = {} ];".format(node, label)  # , node, "[", "label =", label, "];"
    # print connections
    for (n1, n2) in connections:
        data += "\n{} -> {} ;".format(n1, n2)  # + n1, "->", n2, ";")
    data += "\n}"
    return data
