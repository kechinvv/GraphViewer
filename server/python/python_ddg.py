import ast
import numbers
import re
from uuid import uuid4 as uuid

import graphviz as gv


def get_deps(code):
    body = ast.parse(code)
    _, statements = next(ast.iter_fields(body))

    # Line no. at which each identifier was first seen
    declaration_line_num_map = {}
    ddg = {}

    def update_decls(lhs_vars_input, num):
        lhs_var_nodes = []
        for var_node in lhs_vars_input:
            lhs_var_nodes.append(var_node)
            if var_node.id not in declaration_line_num_map:
                declaration_line_num_map[var_node.id] = num
                ddg[var_node.id] = set()
        return lhs_var_nodes

    # x1, x2, x3, ..., xN = 1, 2, 3, 4, 5, ..., N
    # is represented in the AST as:
    #   - R = ast.Assign is root
    #   - R.targets gives the LHS
    #   - R.values

    for seq_no, node in enumerate(statements):
        if isinstance(node, ast.Assign):
            identifier_names = node.targets
            lhs_vars = update_decls(identifier_names, seq_no)

            self_edge_occurrences_to_ignore = {x: 1 for x in identifier_names}

            # DFS in RHS
            depends_on = []
            for descendant in ast.walk(node):
                if descendant in self_edge_occurrences_to_ignore and self_edge_occurrences_to_ignore[descendant] > 0:
                    self_edge_occurrences_to_ignore[descendant] -= 1
                    continue
                if isinstance(descendant, ast.Name):
                    depends_on.append(descendant)

            for var in lhs_vars:
                for dependency in depends_on:
                    ddg[var.id].add(dependency.id)

    return declaration_line_num_map, ddg


class MethodLevelDDGs:
    def __init__(self, code):
        self.parsed_ast = ast.parse(code)

    def get_methods(self):
        fn_nodes = []

        class FnVisitor(ast.NodeVisitor):
            def visit_FunctionDef(self, node):
                fn_nodes.append(node)

        visitor = FnVisitor()
        visitor.visit(self.parsed_ast)
        return fn_nodes

    def recursive_ddg(self, fn_root_node):
        ddg = {}
        self_edge_set = set()

        class DDGVisitor(ast.NodeVisitor):
            def visit_Assign(self, node):
                identifiers = node.targets
                for identifier in identifiers:
                    ddg[identifier.id] = set()
                    self_edge_set.add(identifier.id)

                depends_on = []
                for descendant in ast.walk(node):
                    if isinstance(descendant, ast.Name):
                        depends_on.append(descendant)

                for var in identifiers:
                    for dependency in depends_on:
                        if var.id in self_edge_set:
                            self_edge_set.remove(var.id)
                            continue
                        ddg[var.id].add(dependency.id)

        visitor = DDGVisitor()
        visitor.visit(fn_root_node)
        return ddg


def fn_ddgs(code):
    method_level_ddgs = MethodLevelDDGs(code)
    methods = method_level_ddgs.get_methods()
    ddgs = {method.name: method_level_ddgs.recursive_ddg(method) for method in methods}
    return ddgs




class GraphRenderer:
    """
    this class is capable of rendering data structures consisting of
    dicts and lists as a graph using graphviz
    """

    graphattrs = {
        'labelloc': 't',
        'fontcolor': 'black',
        'bgcolor': 'white',
        'margin': '0',
    }

    nodeattrs = {
        'color': 'black',
        'fontcolor': 'black',
        'style': 'filled',
        'fillcolor': 'white',
    }

    edgeattrs = {
        'color': 'black',
        'fontcolor': 'black',
    }

    _graph = None
    _rendered_nodes = None

    @staticmethod
    def _escape_dot_label(str):
        return str.replace("\\", "\\\\").replace("|", "\\|").replace("<", "\\<").replace(">", "\\>")

    def _render_node(self, node):
        if isinstance(node, (str, numbers.Number)) or node is None:
            node_id = uuid()
        else:
            node_id = id(node)
        node_id = str(node_id)

        if node_id not in self._rendered_nodes:
            self._rendered_nodes.add(node_id)
            if isinstance(node, dict):
                self._render_dict(node, node_id)
            elif isinstance(node, list):
                self._render_list(node, node_id)
            else:
                self._graph.node(node_id, label=self._escape_dot_label(str(node)))

        return node_id

    def _render_dict(self, node, node_id):
        self._graph.node(node_id, label=node.get("node_type", "[dict]"))
        for key, value in node.items():
            if key == "node_type":
                continue
            child_node_id = self._render_node(value)
            self._graph.edge(node_id, child_node_id, label=self._escape_dot_label(key))

    def _render_list(self, node, node_id):
        self._graph.node(node_id, label="[list]")
        for idx, value in enumerate(node):
            child_node_id = self._render_node(value)
            self._graph.edge(node_id, child_node_id, label=self._escape_dot_label(str(idx)))

    def render(self, data, *, label=None):
        # create the graph
        graphattrs = self.graphattrs.copy()
        if label is not None:
            graphattrs['label'] = self._escape_dot_label(label)
        graph = gv.Digraph(graph_attr=graphattrs, node_attr=self.nodeattrs, edge_attr=self.edgeattrs)

        # recursively draw all the nodes and edges
        self._graph = graph
        self._rendered_nodes = set()
        self._render_node(data)
        self._graph = None
        self._rendered_nodes = None

        return graph


##if __name__ == '__main__':
##    code = open("C:/Users/n_zgr/OneDrive/Рабочий стол/py-data-dependency-graph-master/snippets/sample_1.py").read()
##    print(code)
##    decls, graph = code2ddg.get_deps(code)
##    print("var: line_number map =>")
##    print(decls)
##
##    print("variable data dependence =>")
##    print(graph)
##
##    renderer = GraphRenderer()
##    graph = renderer.render(graph, label=None)
##    graph.format = 'dot'
##    return graph.pipe()


def make(code: str):
    decls, graph = get_deps(code)
    renderer = GraphRenderer()
    graph = renderer.render(graph, label=None)
    graph.format = 'dot'
    return graph.pipe()


if __name__ == '__main__':
    code = open("C:/Users/n_zgr/OneDrive/Рабочий стол/py-data-dependency-graph-master/snippets/sample_1.py").read()
    make(code)

