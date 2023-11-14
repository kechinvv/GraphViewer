
import './App.css'
import CodeEditor from './CodeEditor'
import Flow from './Flow'
import { ReactFlowProvider } from 'reactflow';

function App() {

  return (
    <>
    <CodeEditor></CodeEditor>
    <ReactFlowProvider>
        <Flow/>
    </ReactFlowProvider>
    </>
  )
}

export default App
