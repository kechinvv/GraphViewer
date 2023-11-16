import { memo } from 'react';
import { Handle, Position, } from 'reactflow';
import "./RectangleNode.css"


const RectangleNode = ({ data}) => {
 return (
   <div className="rectangle-node">
     <Handle type="target" position={Position.Top} className="handle"/>
     <div style={{ padding: 10 }}>{data.label}</div>
     <Handle type="source" position={Position.Bottom}  />
   </div>

 );
};

export default memo(RectangleNode);
