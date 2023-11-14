
import {useEffect, useState, useCallback, useMemo} from "react"
import AceEditor from "react-ace"
import debounce from "lodash/debounce";
import { useLazyGetGraphCodeQuery } from './store/api/graph.api'
import {useDispatch} from "react-redux"


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
    `a = a + b`,
    `else:`,
    `a = a - b`,
    `c = a + b`,
].join('\n')



// let delayTimer;
// let wait_for_change_delay = 1500;
// function update_graph() {
//     let language = get_current(document.getElementById("code_box")).toLowerCase();
//     let graph_type = get_current(document.getElementById("graph_box")).toLowerCase();
//     let raw_text = editor.getValue();
//     let code_text = encodeURIComponent(raw_text);
//     let query = `${window.location}view_graph?code=${code_text}&lang=${language}&model=${graph_type}`
//     let message_panel = document.getElementById("console_content");
//     let loading_panel = document.getElementById("loading_panel");
//     let console_content = document.getElementById("console_content");
//     clearTimeout(delayTimer);
//     if (raw_text.trim().length !== 0)
//         delayTimer = setTimeout(async function () {
//             loading_panel.style.setProperty("display", "block");
//             let res = await fetch(query);
//             loading_panel.style.setProperty("display", "none");
//             if (res.status !== 200) {
//                 d3.select('svg').selectAll('*').remove();
//                 let j = await res.json();
//                 message_panel.textContent = j.detail
//             } else {
//                 console_content.textContent = "";
//                 let js = await res.text();
//                 console.log(js);
//                 d3.select("#graph").graphviz().renderDot(js);
//                 d3.select("#graph").graphviz().scale = 1;
//             }
//         }, wait_for_change_delay);
//     return 0;
// }




function CodeEditor() {
    const dispatch = useDispatch()
    // const [themeIsLight, setTheme] = useState(true);
    const [lang, setLang] = useState("python");
    const [code, setCode] = useState(defaultCodeState);


    // make async request to update the graph
    useEffect(() => {
        // call debounced request here
        debouncedSendRequest(encodeURIComponent(code));
    }, [code]);

    const [trigger, result, lastPromiseInfo] = useLazyGetGraphCodeQuery()
    useEffect(() => {
        dispatch(setNodes(result.nodes))
        dispatch(setEdges(result.edges))

        console.log(result.error)
    }, [result]);

    const sendBackendRequest = useCallback((value) => {
        trigger(code, lang, "cfg")
      }, []);

    const debouncedSendRequest = useMemo(() => {
        return debounce(sendBackendRequest, 1000);
      }, [sendBackendRequest]);
    
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
                    height="1000px"
                    width="1000px"
                    setOptions={{
                        useWorker: false
                    }}
                    mode={lang}
                    theme={"monokai"}
                    onChange={(e) => setCode(e)}
                />
            </div>
        </div>
    )
}
export default CodeEditor
