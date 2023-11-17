from enum import auto
from pydantic import BaseModel
from .converter import Graph, Edge, Node
from fastapi_utils.enums import CamelStrEnum


class NodeType(CamelStrEnum):
    RHOMBUS = auto()
    RECTANGLE = auto()
    ELLIPSE = auto()


class V2GetGraphRequest(BaseModel):
    code: str
    lang: str
    model: str


class V2Edge(BaseModel):
    id: str
    source: str
    target: str
    style: str


class V2Label(BaseModel):
    label: str


class V2Node(BaseModel):
    id: str
    data: V2Label
    type: NodeType
    lvl: int
    position: dict[str, float]


class V2Graph(BaseModel):
    name: str
    nodes: list[V2Node]
    edges: list[V2Edge]


class V2GetGraphResponse(BaseModel):
    graph: V2Graph


def map_to_response(graph: Graph) -> V2GetGraphResponse:
    return V2GetGraphResponse(graph=map_to_v2graph(graph))


def map_to_v2graph(graph: Graph) -> V2Graph:
    nodes = list(map(map_node, graph.nodes))
    edges = list(map(map_edge, graph.edges))

    v2graph = V2Graph(
        name=graph.name,
        nodes=nodes,
        edges=edges)

    return v2graph


def map_node(node: Node) -> V2Node:
    label = V2Label(label=node.label)
    shape = map_shape(node.shape)

    model = V2Node(id=node.id,
                   data=label,
                   type=shape,
                   lvl=node.lvl,
                   position={"x": node.x, "y": node.y})

    return model


def map_shape(shape: str) -> NodeType:
    match shape:
        case "Mdiamond":
            return NodeType.RHOMBUS
        case "record":
            return NodeType.RECTANGLE
        case "box":
            return NodeType.RECTANGLE
        case "rect":
            return NodeType.RECTANGLE
        case "rectangle":
            return NodeType.RECTANGLE
        case "square":
            return NodeType.RECTANGLE
        case "ellipse":
            return NodeType.ELLIPSE
        case "oval":
            return NodeType.ELLIPSE
        case _:
            return NodeType.RECTANGLE


def map_edge(edge: Edge) -> V2Edge:
    model = V2Edge(id=edge.id, source=edge.source, target=edge.destination, style=edge.style)

    return model
