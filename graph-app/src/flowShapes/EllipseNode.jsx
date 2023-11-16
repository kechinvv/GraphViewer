import { memo } from 'react';
import { Handle, Position, } from 'reactflow';
import "./EllipseNode.css"


const EllipseNode = ({ data}) => {
 return (
  <div className="ellipse-node">
    <Handle type="target" position={Position.Top} className="handle"/>
      <div style={{ padding: 10 }}>{data.label}</div>
    <Handle type="source" position={Position.Bottom}  />
  </div>

 );
};

export default memo(EllipseNode);