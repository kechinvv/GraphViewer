from io import BytesIO
from xml.dom import minidom
from copy import copy

import pydot
import json
import queue


class Node:
    def __init__(self, node_id, label, shape):
        self.id = node_id
        self.label = label
        self.shape = shape
        self.lvl = -1
        self.x = 0.0
        self.y = 0.0

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_lvl(self, lvl):
        self.lvl = lvl


class Edge:
    def __init__(self, source, destination, style):
        self.source = source
        self.destination = destination
        self.style = style


class Graph:
    def __init__(self, name, nodes, edges):
        self.name = name
        self.nodes = nodes
        self.edges = edges


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
        dot_string = dot_to_str(dot)

        graphs = pydot.graph_from_dot_data(dot_string)
        return graphs[0]

    def get_node_name(name):
        if lang == 'c':
            return name.split(':')[0]

        return name

    def bfs(node, edges, start_counter_value, nodes_dict):
        nodes_queue = queue.Queue()
        nodes_queue.put(node)
        counter = start_counter_value
        processed_nodes = set()
        while not nodes_queue.empty():
            current_node = nodes_queue.get()
            processed_nodes.add(current_node.id)
            current_node.set_lvl(counter)
            counter += 1

            for edge in edges:
                if edge.source != current_node.id:
                    continue

                if edge.destination not in processed_nodes:
                    nodes_queue.put(nodes_dict[edge.destination])

        return counter

    def get_text_from_tag(nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)

    def get_copy_nodes(graph_solo):
        nodes = copy(graph_solo.nodes)
        return nodes

    def get_real_nodes(graph_solo):
        nodes = graph_solo.nodes
        return nodes

    def add_lvl(graph_full):
        nodes_dict = {}
        for node in get_copy_nodes(graph_full):
            nodes_dict[node.id] = node
        counter = 1
        for node in graph_full.nodes:
            if node.lvl != -1:
                continue

            counter = bfs(node, graph_full.edges, counter, nodes_dict)

    def add_positions(graph_full, d_graph):
        svg_io = BytesIO(d_graph.create_svg())
        d_graph.write_svg("./test.svg")
        doc = minidom.parse(svg_io)
        nodes = get_real_nodes(graph_full)
        node_mapping = {dot_node.id.replace('\"', ''): dot_node for dot_node in nodes}
        for p in doc.getElementsByTagName("g"):
            if "node" == p.getAttribute('class').lower():
                title = get_text_from_tag(p.getElementsByTagName('title')[0].childNodes)
                if title not in node_mapping.keys():
                    continue
                for c_text in p.getElementsByTagName('text'):
                    node_mapping[title].x = float(c_text.getAttribute('x'))
                    node_mapping[title].y = float(c_text.getAttribute('y'))
                    break

        doc.unlink()

    def dot_graph_to_graph(graph) -> Graph:
        # nodes_with_edges = set()
        edges = []
        name = graph.get_name()
        for dot_edge in graph.get_edges():
            source = get_node_name(dot_edge.get_source())
            destination = get_node_name(dot_edge.get_destination())
            style = dot_edge.get_attributes().get("style", EDGE_STYLE_DEFAULT_VALUE)

            edge = Edge(source, destination, style)
            edges.append(edge)

            # nodes_with_edges.add(edge.source)
            # nodes_with_edges.add(edge.destination)

        nodes = []
        for dot_node in graph.get_nodes():
            id = dot_node.get_name()

            # if id not in nodes_with_edges:
            #    continue

            label = dot_node.get_attributes().get("label", LABEL_DEFAULT_VALUE)
            shape = dot_node.get_attributes().get("shape", SHAPE_DEFAULT_VALUE)

            node = Node(id, label, shape)
            nodes.append(node)

        for dot_subgraph in graph.get_subgraphs():
            subgraph = dot_graph_to_graph(dot_subgraph)
            nodes += subgraph.nodes
            edges += subgraph.edges

        return Graph(name, nodes, edges)

    def filter_nodes_without_links(full_graph):
        used_nodes_id = set()
        for e in full_graph.edges:
            used_nodes_id.add(e.source)
            used_nodes_id.add(e.destination)
        in_use_nodes = filter(lambda n: n.id in used_nodes_id, full_graph.nodes)
        full_graph.nodes = list(in_use_nodes)

    gv_graph = dot_to_graph(dot_graph)
    graph = dot_graph_to_graph(gv_graph)

    filter_nodes_without_links(graph)
    add_lvl(graph)
    add_positions(graph, gv_graph)

    return graph
