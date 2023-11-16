
import { useEffect, useState, useCallback, useMemo } from "react"
import AceEditor from "react-ace"
import debounce from "lodash/debounce";
import { useLazyGetGraphCodeQuery } from './store/api/graph.api'
import { useDispatch, useSelector } from "react-redux"

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

const languages = [
    "javascript",
    "java",
    "python",
    "kotlin",
    "c_cpp",
    "golang",
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
    // const [themeIsLight, setTheme] = useState(true);
    const [lang, setLang] = useState("python");
    const [code, setCode] = useState(defaultCodeState);
    const [model, setModel] = useState("ast")

    const [trigger, result, lastPromiseInfo] = useLazyGetGraphCodeQuery()
    useEffect(() => {
        if (result.data) {
            const graph = result.data.graph
            dispatch(setNodes(graph.nodes))
            dispatch(setEdges(graph.edges))
        }
    }, [result]);


    useSelector(state => {
        console.log(state.graph)
    })
    const sendBackendRequest = useCallback((code, lang, model) => {
        trigger({ code, lang, model})
    }, []);

    const debouncedSendRequest = useMemo(() => {
        return debounce(sendBackendRequest, 1500);
    }, [sendBackendRequest]);

    // make async request to update the graph
    useEffect(() => {
        // call debounced request here
        debouncedSendRequest(code, lang, model);
    }, [code, lang, model]);

    return (
        <div className="columns">
            <div className="column">
                <div className="field">
                    <label>Mode:</label>
                    <p className="control">
                        <span className="select">
                            <select
                                name="mode"
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
                </div>

                <div className="field" />
            </div>
            <div className="examples column">
                <h2>Editor</h2>
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
