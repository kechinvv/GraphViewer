import pydot
import json


class Node:
    def __init__(self, id, label, shape):
        self.id = id
        self.label = label
        self.shape = shape


class Edge:
    def __init__(self, source, destination, style):
        self.source = source
        self.destination = destination
        self.style = style


class Graph:
    def __init__(self, name, nodes, edges, subgraphs):
        self.name = name
        self.nodes = nodes
        self.edges = edges
        self.subgraphs = subgraphs


class GraphEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


def convert_dot_to_json(dot_graph, lang):
    LABEL_DEFAULT_VALUE = ""
    SHAPE_DEFAULT_VALUE = "ellipse"
    EDGE_STYLE_DEFAULT_VALUE = "solid"

    def dot_to_str(dot):
        if type(dot) is str:
            return dot

        if type(dot) is bytes:
            return str(dot, encoding='utf-8')

        raise Exception

    def dot_to_graph(dot):
        dot_string = dot_to_str(dot_graph)

        graphs = pydot.graph_from_dot_data(dot_string)
        return graphs[0]

    def get_node_name(name):
        if lang == 'c':
            return name.split(':')[0]

        return name

    def dot_graph_to_graph(graph):
        #nodes_with_edges = set()
        edges = []
        name = graph.get_name()
        for dot_edge in graph.get_edges():
            source = get_node_name(dot_edge.get_source())
            destination = get_node_name(dot_edge.get_destination())
            style = dot_edge.get_attributes().get("style", EDGE_STYLE_DEFAULT_VALUE)

            edge = Edge(source, destination, style)
            edges.append(edge)

            #nodes_with_edges.add(edge.source)
            #nodes_with_edges.add(edge.destination)

        nodes = []
        for dot_node in graph.get_nodes():
            id = dot_node.get_name()

            #if id not in nodes_with_edges:
            #    continue

            label = dot_node.get_attributes().get("label", LABEL_DEFAULT_VALUE)
            shape = dot_node.get_attributes().get("shape", SHAPE_DEFAULT_VALUE)

            node = Node(id, label, shape)
            nodes.append(node)

        subgraphs = []
        for dot_subgraph in graph.get_subgraphs():
            subgraph = dot_graph_to_graph(dot_subgraph)
            subgraphs.append(subgraph)

        return Graph(name, nodes, edges, subgraphs)

    def graph_to_json(graph):
        return GraphEncoder().encode(graph)

    return graph_to_json(dot_graph_to_graph(dot_to_graph(dot_graph)))
