
import { useState, useEffect } from "react";
import ReactFlow from "react-flow-renderer";
import { useNodesState, useEdgesState, MarkerType } from "reactflow"

import { useSelector } from "react-redux"
import RectangleNode from "./flowShapes/RectangleNode";
import RhombusNode from "./flowShapes/RhombusNode";
import EllipseNode from "./flowShapes/EllipseNode";
import elkLayout from "./elkLayout";
import { SmartBezierEdge } from '@tisoap/react-flow-smart-edge'

const nodeTypes = {
    rectangle: RectangleNode,
    rhombus: RhombusNode,
    ellipse: EllipseNode
};

const edgeTypes = {
    smart : SmartBezierEdge
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
            setNodes(initialNodes);
            setEdges(noGraphEdgesForFlow(initialEdges));
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
