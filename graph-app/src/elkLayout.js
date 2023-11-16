import ELK from "elkjs";


const elkLayout = (initialNodes, initialEdges) => {
    const elk = new ELK();
  const nodesForElk = initialNodes.map((node) => {
    return {
      id: node.id,
      width: node.type === "rectangle" ? 100 : 100,
      height: node.type === "rhombus" ? 100 : 100
    };
  });
  const graph = {
    id: "root",
    layoutOptions: {
      "elk.algorithm": "layered",
      "elk.direction": "DOWN",
      "nodePlacement.strategy": "SIMPLE"
    },

    children: nodesForElk,
    edges: initialEdges
  };
  return elk.layout(graph);
};

export default elkLayout;
