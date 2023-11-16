import { Handle, Position } from "react-flow-renderer";
import "./RhombusNode.css"
import { memo } from 'react';

function calculateDimensions(text) {
    // Create a temporary div element
    const tempDiv = document.createElement('div');

    // Set the div's text to the label
    tempDiv.innerHTML = text;

    // Apply the same styles as the rhombus content
    tempDiv.style.display = 'inline-block';
    tempDiv.style.visibility = 'hidden';
    document.body.appendChild(tempDiv);

    // Get the dimensions of the div
    const maxDim = Math.max(tempDiv.offsetWidth, tempDiv.offsetHeight) * 2

    // Remove the temporary div from the document
    document.body.removeChild(tempDiv);

    return maxDim;
}

const RhombusleNode = ({ data }) => {
    // Calculate the dimensions of the label text
    const maxDim = calculateDimensions(data.label);

    // Apply these dimensions to the rhombus-node
    const rhombusStyle = {
        width: `${maxDim}px`,
        height: `${maxDim}px`,
    };
    const containerSize = (4.8 * maxDim)/ 3.8

    return (
        <div className="handles-container" style={{height: `${containerSize}px`}}>
            <div className="rhombus-node" style={rhombusStyle}></div>
            <Handle type="target" position={Position.Top} className="handle" />
            <div className="rhombus-content">{data.label}</div>
            <Handle type="source" position={Position.Bottom} />
        </div>

    );
};

export default memo(RhombusleNode);