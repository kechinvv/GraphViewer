
import './App.css'
import CodeEditor from './CodeEditor'
import Flow from './Flow'
import { ReactFlowProvider } from 'reactflow';

function App() {

  return (
    <div className="topDiv">
    <CodeEditor></CodeEditor>
    <ReactFlowProvider>
        <Flow/>
    </ReactFlowProvider>
    </div>
  )
}

export default App
