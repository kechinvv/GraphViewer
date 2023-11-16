import { memo } from 'react';
import { Handle, Position, } from 'reactflow';
import "./RectangleNode.css"
import { VscArchive } from "react-icons/vsc";


const RectangleNode = ({ data }) => {
 return (
   <div className="rectangle-node">
     <Handle type="target" position={Position.Top} className="handle"/>
     <div style={{ padding: 10 }}>{data.label}{data.hasHidden ? <VscArchive/>: ''}</div>
     <Handle type="source" position={Position.Bottom}  />
   </div>

 );
};

export default memo(RectangleNode);
