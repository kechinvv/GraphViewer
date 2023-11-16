
import { useState, useEffect } from "react";
import ReactFlow from "react-flow-renderer";
import { useNodesState, useEdgesState, MarkerType } from "reactflow"

import { useSelector } from "react-redux"
import RectangleNode from "./flowShapes/RectangleNode";
import RhombusNode from "./flowShapes/RhombusNode";
import elkLayout from "./elkLayout";
import { SmartBezierEdge } from '@tisoap/react-flow-smart-edge'

const nodeTypes = {
    rectangleNode: RectangleNode,
    rhombusNode: RhombusNode
};

const edgeTypes = {
    smart : SmartBezierEdge
};

function Flow() {

    const { nodes: initialNodes, edges: initialEdges } = useSelector(state => state.graph)

    const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
    const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

    const nodesForFlow = (graph) => {
        return [
            ...graph.children.map((node) => {
                return {
                    ...initialNodes.find((n) => n.id === node.id),
                    position: { x: node.x, y: node.y }
                };
            })
        ];
    };
    const edgesForFlow = (graph) => {
        return [
            ...graph.edges.map((edge) => {
                return {
                    ...edge,
                    type: 'smart',
                    markerEnd: {
                        type: MarkerType.ArrowClosed,
                        width: 20,
                        height: 20,
                        color: '#FFFFFF',
                      },
                };
            })
        ];
    };

    useEffect(() => {
        if (Array.isArray(initialNodes) && Array.isArray(initialEdges)) {
            elkLayout(initialNodes.map(node => ({ ...node })), initialEdges.map(node => ({ ...node }))).then((graph) => {
                setNodes(nodesForFlow(graph));
                setEdges(edgesForFlow(graph));
            });
        }

    }, [initialNodes, initialEdges])


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
        fitView />
    );
}

export default Flow;
