
import { useEffect, useState, useCallback, useMemo } from "react"
import AceEditor from "react-ace"
import debounce from "lodash/debounce";
import { useLazyGetGraphCodeQuery } from './store/api/graph.api'
import { useDispatch } from "react-redux"
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// highlight imports
import "ace-builds/src-noconflict/mode-python"
import "ace-builds/src-noconflict/mode-javascript"
import "ace-builds/src-noconflict/mode-java"
import "ace-builds/src-noconflict/mode-kotlin"
import "ace-builds/src-noconflict/mode-c_cpp"
import "ace-builds/src-noconflict/mode-golang"

// theme imports
// dark theme
import "ace-builds/src-noconflict/theme-monokai"
// loght theme
import "ace-builds/src-noconflict/theme-github"
import { setEdges, setNodes } from "./features/graph/graphSlice";
import { setModel } from "./features/graph/modelSlice";

const languages = [
    "javascript",
    "java",
    "python",
    "kotlin",
    "c_cpp",
    "golang",
];

const models = [
    "ast",
    "cfg",
];



let defaultCodeState = [
    `a = 2`,
    `b = 3`,
    `if a > b:`,
    `   a = a + b`,
    `else:`,
    `   a = a - b`,
    `c = a + b`,
].join('\n')




function CodeEditor() {
    const dispatch = useDispatch()

    const [lang, setLang] = useState("python");
    const [code, setCode] = useState(defaultCodeState);
    const [model, setModel] = useState("ast")


    const [trigger, result, lastPromiseInfo] = useLazyGetGraphCodeQuery()
    useEffect(() => {
        if (!result.isError && result.data) {
            const graph = result.data.graph
            dispatch(setNodes(graph.nodes))
            dispatch(setEdges(graph.edges))
        } else if (result.isError) {
            if (result.error.data) {
                toast.error(result.error.data, {
                    closeOnClick: true,
                    pauseOnHover: true,
                });
                toast.error(result.error.data.detail, {
                    position: "top-right",
                    autoClose: 5000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                    theme: "light",
                });
            } else {
                toast.error("Something bad happened, I don't", {
                    closeOnClick: true,
                    pauseOnHover: true,
                });
            }

        }
    }, [result]);

    // useEffect (() => dispatch(setModel(model)), [model])

    const sendBackendRequest = useCallback((code, lang, model) =>  trigger({ code, lang, model }), []);

    const debouncedSendRequest = useMemo(() => {
        return debounce(sendBackendRequest, 1500);
    }, [sendBackendRequest]);

    // make async request to update the graph
    useEffect(() => {
        // call debounced request here
        debouncedSendRequest(code, lang, model);
    }, [code, lang, model]);

    return (
        <div className="columns super-editor">
            <div className="column">
                <div className="field">
                    <div className="mode">Mode:</div>
                    <div className="mode-control">
                        <p className="control">
                            <span className="select">
                                
                                <select
                                    name="lang"
                                    onChange={(e) => setLang(e.target.value)}
                                    value={lang}
                                >
                                    {languages.map(lang => (
                                        <option key={lang} value={lang}>
                                            {lang}
                                        </option>
                                    ))}
                                </select>
                            </span>
                        </p>
                        <p className="control">
                            <span className="select">
                                <select
                                    name="model"
                                    onChange={(e) => setModel(e.target.value)}
                                    value={model}
                                >
                                    {models.map(model => (
                                        <option key={model} value={model}>
                                            {model}
                                        </option>
                                    ))}
                                </select>
                            </span>
                        </p>
                    </div>
                </div>

                <div className="field" />
            </div>
            <ToastContainer
                position="top-right"
                autoClose={5000}
                hideProgressBar={false}
                newestOnTop
                closeOnClick
                rtl={false}
                pauseOnFocusLoss={false}
                draggable
                pauseOnHover={false}
                theme="light"
            />
            <div className="examples column">
                <AceEditor
                    value={code}
                    setOptions={{
                        useWorker: false
                    }}
                    mode={lang}
                    theme={"github"}
                    onChange={(e) => setCode(e)}
                />
            </div>
        </div>
    )
}
export default CodeEditor
