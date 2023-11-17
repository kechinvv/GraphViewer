from enum import auto
from pydantic import BaseModel
from .converter_with_sub import Graph, Edge, Node
from fastapi_utils.enums import CamelStrEnum


class NodeType(CamelStrEnum):
    RHOMBUS = auto()
    RECTANGLE = auto()
    ELLIPSE = auto()


class V1GetGraphRequest(BaseModel):
    code: str
    lang: str
    model: str


class V1Edge(BaseModel):
    source: str
    target: str
    style: str


class V1Label(BaseModel):
    label: str


class V1Node(BaseModel):
    id: str
    data: V1Label
    type: NodeType
    lvl: int


class V1Graph(BaseModel):
    name: str
    nodes: list[V1Node]
    edges: list[V1Edge]
    subgraphs: list


class V1GetGraphResponse(BaseModel):
    graph: V1Graph


def map_to_v1response(graph: Graph) -> V1GetGraphResponse:
    return V1GetGraphResponse(graph=map_to_v1graph(graph))


def map_to_v1graph(graph: Graph) -> V1Graph:
    nodes = list(map(map_node, graph.nodes))
    edges = list(map(map_edge, graph.edges))
    subgraphs = list(map(map_to_v1graph, graph.subgraphs))

    v1graph = V1Graph(
        name=graph.name,
        nodes=nodes,
        edges=edges,
        subgraphs=subgraphs)

    return v1graph


def map_node(node: Node) -> V1Node:
    label = V1Label(label=node.label)
    shape = map_shape(node.shape)

    model = V1Node(id=node.id, data=label, type=shape, lvl=node.lvl)

    return model


def map_shape(shape: str) -> NodeType:
    match shape:
        case "Mdiamond":    return NodeType.RHOMBUS
        case "record":      return NodeType.RECTANGLE
        case "box":         return NodeType.RECTANGLE
        case "rect":        return NodeType.RECTANGLE
        case "rectangle":   return NodeType.RECTANGLE
        case "square":      return NodeType.RECTANGLE
        case "ellipse":     return NodeType.ELLIPSE
        case "oval":        return NodeType.ELLIPSE
        case _:             return NodeType.RECTANGLE


def map_edge(edge: Edge) -> V1Edge:
    model = V1Edge(source=edge.source, target=edge.destination, style=edge.style)

    return model
