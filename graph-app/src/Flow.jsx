
import { useState, useEffect } from "react";
import ReactFlow from "react-flow-renderer";
import { useNodesState, useEdgesState, MarkerType, getOutgoers, getConnectedEdges } from "reactflow"

import { useSelector } from "react-redux"
import RectangleNode from "./flowShapes/RectangleNode";
import RhombusNode from "./flowShapes/RhombusNode";
import EllipseNode from "./flowShapes/EllipseNode";
import { SmartBezierEdge } from '@tisoap/react-flow-smart-edge'

const nodeTypes = {
    rectangle: RectangleNode,
    rhombus: RhombusNode,
    ellipse: EllipseNode
};

const edgeTypes = {
    smart: SmartBezierEdge
};

const markerEnd = {
    type: MarkerType.ArrowClosed,
    width: 20,
    height: 20,
    color: '#FFFFFF',
}

function Flow() {

    const { nodes: initialNodes, edges: initialEdges } = useSelector(state => state.graph)

    const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
    const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

    // autolayouting is now done on server
    // features related to autolayouting
    // const nodesForFlow = (graph) => {
    //     return [
    //         ...graph.children.map((node) => {
    //             return {
    //                 ...initialNodes.find((n) => n.id === node.id),
    //                 position: { x: node.x, y: node.y }
    //             };
    //         })
    //     ];
    // };
    // const edgesForFlow = (graph) => {
    //     return [
    //         ...graph.edges.map((edge) => {
    //             return {
    //                 target: edge.target,
    //                 source: edge.source,
    //                 id: edge.id,
    //                 markerEnd: {
    //                     type: MarkerType.ArrowClosed,
    //                     width: 20,
    //                     height: 20,
    //                     color: '#FFFFFF',
    //                   },
    //             };
    //         })
    //     ];
    // };

    const nodesForFlow = (nodes) => {
            return [
                ...nodes.map((node) => {
                    return {
                        ...node,
                        data: {
                            ...node.data,
                            hasHidden: false,
                        }
                        
                    };
                })
            ];
        };

    const noGraphEdgesForFlow = (edges) => {
        return [
            ...edges.map((edge) => {
                return {
                    target: edge.target,
                    source: edge.source,
                    id: edge.id,
                    markerEnd: markerEnd
                };
            })
        ];
    };

    useEffect(() => {
        if (Array.isArray(initialNodes) && Array.isArray(initialEdges)) {
            // autolayouting is deprecated
            // elkLayout(initialNodes.map(node => ({ ...node })), initialEdges.map(node => ({ ...node }))).then((graph) => {
            //     setNodes(nodesForFlow(graph));
            //     setEdges(edgesForFlow(graph));
            // });
            setNodes(nodesForFlow(initialNodes));
            setEdges(noGraphEdgesForFlow(initialEdges));
        }

    }, [initialNodes, initialEdges])

    const hide = (isHiding, childEdgeIDs, childNodeIDs, rootID, isNode) => (nodeOrEdge) => {
        if (
            childEdgeIDs.includes(nodeOrEdge.id) ||
            childNodeIDs.includes(nodeOrEdge.id)
        ) {
            nodeOrEdge.hidden = isHiding;
            if (isNode) {
                nodeOrEdge.data.hasHidden = isHiding
            }
        }
           
        if (nodeOrEdge.id === rootID) {
            nodeOrEdge.data.hasHidden = isHiding
        }

        return nodeOrEdge;
    };

    const checkTarget = (edge, id) => {
        let edges = edge.filter((ed) => {
            return ed.target !== id;
        });
        return edges;
    };

    let outgoers = [];
    let connectedEdges = [];
    let stack = [];

    const nodeClick = (some, node) => {
        console.log(node)
        let currentNodeID = node.id;
        stack.push(node);

        let firstPass = true
        let isHiding = true
        while (stack.length > 0) {
            let lastNOde = stack.pop();
            let childnodes = getOutgoers(lastNOde, nodes, edges);
            if (firstPass && childnodes.every((node) => node.hidden)) {
                isHiding = false
            }

            let childedges = checkTarget(
                getConnectedEdges([lastNOde], edges),
                currentNodeID
            );
            childnodes.map((goer, key) => {
                stack.push(goer);
                outgoers.push(goer);
            });
            childedges.map((edge, key) => {
                connectedEdges.push(edge);
            });
            firstPass = false
        }

        let childNodeIDs = outgoers.map((node) => {
            return node.id;
        });
        let childEdgeIDs = connectedEdges.map((edge) => {
            return edge.id;
        });

        // node.isHidden = !node.isHidden

        setNodes((nodes) => nodes.map(hide(isHiding, childEdgeIDs, childNodeIDs, node.id, true)));
        setEdges((edges) => edges.map(hide(isHiding, childEdgeIDs, childNodeIDs, node.id, false)));
    };

    if (nodes === null) {
        return <></>;
    }

    return (
        <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            nodeTypes={nodeTypes}
            edgeTypes={edgeTypes}
            onNodeClick={nodeClick}
            fitView />
    );
}

export default Flow;
