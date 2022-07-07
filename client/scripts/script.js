/*CODE SECTION SCRIPTS*/

var theme_is_dark = false;
var editor = ace.edit("code");
editor.setTheme("ace/theme/cloud9_day");
editor.setOptions({
  fontSize: "14pt"
});
editor.focus();

var PythonMode = ace.require("ace/mode/python").Mode;
var KotlinMode = ace.require("ace/mode/kotlin").Mode;
var JavaMode = ace.require("ace/mode/java").Mode;
var GoMode = ace.require("ace/mode/golang").Mode;
var CMode = ace.require("ace/mode/c_cpp").Mode;
var JSMode = ace.require("ace/mode/javascript").Mode;
editor.session.setMode(new PythonMode());
editor.setShowPrintMargin(false);

function toggle_code_theme(button) {
    let icon = document.getElementById("ThemeIcon");
    let console_content = document.getElementById("console_content");
    if (theme_is_dark) {
        editor.setTheme("ace/theme/cloud9_day");
        icon.src="/client/images/night_light.svg";
        button.style.setProperty("color", "white");
        button.style.setProperty("background", "#414047");
        console_content.style.setProperty("background", "white");
    } else {
        editor.setTheme("ace/theme/cloud9_night");
        icon.src="/client/images/day_dark.svg";
        button.style.setProperty("color", "#414047");
        button.style.setProperty("background", "white");
        console_content.style.setProperty("background", "#181819FF");
    }
    theme_is_dark = !theme_is_dark;
}

function configure_code_section(language) {
    switch (language) {
        case "Python":
            editor.session.setMode(new PythonMode());
            break
        case "Kotlin":
            editor.session.setMode(new KotlinMode());
            break
        case "Java":
            editor.session.setMode(new JavaMode());
            break
        case "Go":
            editor.session.setMode(new GoMode());
            break
        case "C":
            editor.session.setMode(new CMode());
            break
        case "JS":
            editor.session.setMode(new JSMode());
            break
    }
}


let delayTimer;
let wait_for_change_delay = 1500;
function update_graph() {
    let language = get_current(document.getElementById("code_box")).toLowerCase();
    let graph_type = get_current(document.getElementById("graph_box")).toLowerCase();
    let raw_text = editor.getValue();
    let code_text = encodeURIComponent(raw_text);
    let query = `${window.location}view_graph?code=${code_text}&lang=${language}&model=${graph_type}`
    let message_panel = document.getElementById("console_content");
    let loading_panel = document.getElementById("loading_panel");
    clearTimeout(delayTimer);
    if (raw_text.trim().length !== 0)
        delayTimer = setTimeout(async function () {
            loading_panel.style.setProperty("display", "block");
            let res = await fetch(query);
            loading_panel.style.setProperty("display", "none");
            if (res.status !== 200) {
                d3.select('svg').selectAll('*').remove();
                let j = await res.json();
                message_panel.textContent = j.detail
            } else {
                let js = await res.text();
                console.log(js);
                d3.select("#graph").graphviz().renderDot(js);
                d3.select("#graph").graphviz().scale = 1;
            }
        }, wait_for_change_delay);
    return 0;
}

editor.on('change', function() {
    update_graph()
})
/*---------------------------------------*/

/*RESIZER SCRIPTS*/

const ExpandMode = {CODE: "code", GRAPH: "graph", MIDDLE: "middle", CUSTOM: "custom"};
var currentExpandMode = ExpandMode.MIDDLE;

function toggle_expand_mode(selectedExpandMode) {
    if (currentExpandMode === selectedExpandMode) {
        setExpandMode(ExpandMode.MIDDLE);
    } else {
        setExpandMode(selectedExpandMode);
    }
}

function setExpandMode(expandMode) {
    let code_wrapper = document.getElementById("code_wrapper");
    let code_label = document.getElementById("code_resizer_label");
    let graph_wrapper = document.getElementById("graph_wrapper");
    let graph_label = document.getElementById("graph_resizer_label");
    let console_content = document.getElementById("console_content");
    switch (expandMode) {
        case ExpandMode.CODE:
            code_wrapper.style.setProperty("width", "100%");
            code_label.style.removeProperty("color");
            graph_wrapper.style.setProperty("width", "0%");
            graph_label.style.setProperty("color", "white");
            console_content.style.setProperty("width", "calc(100% - 50px)");
            break
        case ExpandMode.GRAPH:
            code_wrapper.style.setProperty("width", "0%");
            code_label.style.setProperty("color", "white");
            graph_wrapper.style.setProperty("width", "100%");
            graph_label.style.removeProperty("color");
            console_content.style.setProperty("width", "calc(50% - 25px)");
            break
        case ExpandMode.MIDDLE:
            code_wrapper.style.setProperty("width", "100%");
            code_label.style.removeProperty("color");
            graph_wrapper.style.setProperty("width", "100%");
            graph_label.style.removeProperty("color");
            console_content.style.setProperty("width", "calc(50% - 25px)");
            break
    }
    currentExpandMode = expandMode;
}
/*---------------------------------------*/



/*CUSTOM SELECT SCRIPTS*/

initialize_select()


const SelectBoxes = {CODE_BOX: "code_box", GRAPH_BOX: "graph_box"}

var implemented_funcs_dict;


async function initialize_select() {
    let query = `${window.location}functions`;
    let implemented_funcs = await fetch(query);
    implemented_funcs_dict = await implemented_funcs.json();
    update_code_select()
    update_graph_select()
    let code_box = document.getElementById('code_box');
    let graph_box = document.getElementById('graph_box');
    window.addEventListener('click', function(e){
        if (code_box.contains(e.target)) {
            hide_select_body(graph_box);
        }
        else if (graph_box.contains(e.target)) {
            hide_select_body(code_box);
        } else {
            hide_select_body(graph_box);
            hide_select_body(code_box);
        }
        editor.focus();
    });
}

function update_code_select() {
    var select_box = document.getElementById(SelectBoxes.CODE_BOX);
    update_select(select_box, Object.keys(implemented_funcs_dict).map(lang => capitalize(lang)));
}

function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function update_graph_select() {
    var graph_box = document.getElementById(SelectBoxes.GRAPH_BOX);
    var code_box = document.getElementById(SelectBoxes.CODE_BOX);
    var trees = implemented_funcs_dict[get_current(code_box).toLowerCase()];
    if (Array.isArray(trees)) {
        update_select(graph_box, trees.map(lang => lang.toUpperCase()));
    } else {
        update_select(graph_box, [trees].map(lang => lang.toUpperCase()));
    }
}

function update_select(select_box, values) {
    clear_select(select_box);
    add_select(select_box, values);
    update_current(select_box, values[0]);
}

function clear_select(select_box) {
    var ul = select_box.children[1];
    while (ul.firstChild) {
        ul.removeChild(ul.firstChild);
    }
}

function add_select(select_box, values) {
    values.forEach(value => add_option(select_box, value))
}

function add_option(select_box, option) {
    var ul = select_box.children[1];
    var li = document.createElement("li");
    li.appendChild(document.createTextNode(option));
    li.addEventListener("click", function () {
        update_current(select_box, option);
    });
    ul.appendChild(li);
}

function update_load_select(select_box, values) {
    clear_select(select_box);
    add_load_select(select_box, values);
    if (values.length > 0) update_current(select_box, "Select example");
    else update_current(select_box, "No examples found");
}

function add_load_select(select_box, values) {
    values.forEach(value => add_load_option(select_box, value))
}

let current_selected_id;

function add_load_option(select_box, option) {
    var ul = select_box.children[1];
    var li = document.createElement("li");
    li.appendChild(document.createTextNode(option.description));
    li.addEventListener("click", function () {
        update_current(select_box, option.description);
        current_selected_id = option.id;
    });
    ul.appendChild(li);
}

function get_current(select_box) {
    var select_current = select_box.children[0].children[0];
    return select_current.textContent;
}

function update_current(select_box, value) {
    var select_current = select_box.children[0].children[0];
    select_current.textContent = value;
    update_graph();
    if (select_box.id === "code_box") {
        update_graph_select()
    }
}

function toggle_select(select_box) {
    let current_state =  select_box.getAttribute("state");
    if (current_state === "hidden") {
        show_select_body(select_box);
    } else {
        hide_select_body(select_box);
    }
}

function hide_select_body(select_box) {
    select_box.children[1].style.setProperty("display", "none");
    select_box.setAttribute("state", "hidden");
}

function show_select_body(select_box) {
    select_box.children[1].style.setProperty("display", "block");
    select_box.setAttribute("state", "shown");
}

/*---------------------------------------*/

let load_result;
let load_box = document.getElementById('load_box');

async function save() {
    var description = prompt("Enter description");
    if (description.length > 0) {
        let code_box = document.getElementById('code_box');
        var language = get_current(code_box);
        let query = `${window.location}code?language=${language}&code=${encodeURI(editor.getValue())}&description=${encodeURI(description)}`;
        let res = await fetch(query, {method: 'POST'});
    } else {
        alert("Description should not be empty")
        await save();
    }

}

async function load() {
    let query = `${window.location}user_code`;
    await fetch(query)
        .then((response) => response.json())
        .then((users_content) => {
            load_result = users_content;
    });
    update_load_select(load_box, load_result);
}

async function load_selected_example() {
    let query = `${window.location}code?code_id=${current_selected_id}`;
    let res = await fetch(query, {method: 'GET'});
    let result = await res.json();
    editor.setValue(result.code);
    let code_box = document.getElementById('code_box');
    update_current(code_box, result.language);
}

async function delete_selected_example() {
    let agree = confirm("Are you sure to delete this code fragment?");
    if (agree) {
        let query = `${window.location}code?code_id=${current_selected_id}`;
        let res = await fetch(query, {method: 'DELETE'});
        load();
    }
}

let load_panel_is_shown= false;
let load_panel = document.getElementById('load_code_panel');

function toggle_load_panel() {
    if (load_panel_is_shown) {
        load_panel.style.setProperty('display', 'none');
    } else {
        load()
        load_panel.style.setProperty('display', 'flex');
    }
    load_panel_is_shown = !load_panel_is_shown;
}

window.addEventListener('click', function(e){
    if (!load_button.contains(e.target) && !load_panel.contains(e.target)) {
        console.log("hide")
        load_panel.style.setProperty('display', 'none');
        load_panel_is_shown = false;
    }
});

/*---------------------------------------*/


/*LOGIN & LOGOUT SCRIPTS*/

let login_button = document.getElementById("login_button");
let logout_button = document.getElementById("logout_button");
let save_button = document.getElementById("save_button");
let load_button = document.getElementById("load_button");

update_log_in_out()



async function is_logged() {
    let query = `${window.location}whoami`;
    let res = await fetch(query);
    return res.status === 200;
}

async function log_out() {
    let query = `${window.location}exit`;
    let res = await fetch(query);
    await update_log_in_out()

}


async function update_log_in_out() {
    let current_is_logged = await is_logged();
    if (current_is_logged) {
        login_button.style.setProperty("display", "none");
        logout_button.style.setProperty("display", "block");
        save_button.style.setProperty("display", "block");
        load_button.style.setProperty("display", "block");
    } else {
        logout_button.style.setProperty("display", "none");
        login_button.style.setProperty("display", "block");
        save_button.style.setProperty("display", "none");
        load_button.style.setProperty("display", "none");
    }
}

let is_log_shown = true;

function toggle_console_log() {
    let console_content = document.getElementById("console_content");
    let code_content = document.getElementById("code_container");
    if (is_log_shown) {
        console_content.style.setProperty("height", "0");
        code_content.style.setProperty("height", "calc(100% - 40px)");
    } else {
        console_content.style.setProperty("height", "calc(0.25 * (100% - 40px))");
        code_content.style.setProperty("height", "calc(0.75 * (100% - 40px))");
    }
    is_log_shown = !is_log_shown;
}
