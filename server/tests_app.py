from starlette.testclient import TestClient
from app import app, functions

client = TestClient(app)

not_passed = {'python': (), 'kotlin': 'cfg', 'c': ('cfg', 'ssa'), 'go': ('ast', 'cfg'),
              'java': 'cfg', 'js': ('ast', 'cfg')}


def graph_test(code, lang, model, status_code):
    request = '/view_graph?code=' + code + '&lang=' + lang + '&model=' + model
    response = client.get(request)
    print('\nRequest:\t' + request)
    print("Status:\t" + response.reason)
    print(response.text)
    assert response.status_code == status_code


def graph_test_models(code_200, code_400, lang):
    for model in functions[lang]:
        if model not in not_passed[lang]:
            graph_test(code_200, lang, model, 200)
        else:
            graph_test(code_200, lang, model, 400)
        graph_test(code_400, lang, model, 400)


class TestApp:
    def test_root(self):
        response = client.get("/")
        assert response.url == "http://testserver/"
        assert response.status_code == 200

    def test_all_functions(self):
        response = client.get("/functions")
        assert response.status_code == 200
        assert response.json() == {lang: list(model) for lang, model in functions.items()}

    class TestViewGraph:
        def test_python(self):
            lang = 'python'
            graph_test_models(
                "a = 0%0D%0Ab = 2%0D%0Aa += b", "a = 0%0D%0A    b = 2", lang
            )

        def test_kotlin(self):
            lang = 'kotlin'
            graph_test_models(
                "fun main() {%0D%0A    var a = 0;    val b = 2%0D%0A    a += b%0D%0A}",
                "fun main() {%0D%0A    var a = 0    a = 1%0D%0A}", lang
            )

        def test_c(self):
            lang = 'c'
            graph_test_models(
                "int main() {%0D%0A    int a = 0;%0D%0A    int b = 2;%0D%0A    a += b;%0D%0A    return 0;%0D%0A}",
                "int main() {%0D%0A    return 0%0D%0A}", lang
            )

        def test_go(self):
            lang = 'go'
            graph_test_models(
                "int main() {%0D%0A    int a = 0;%0D%0A    int b = 2;%0D%0A    a += b;%0D%0A    return 0;%0D%0A}",
                "int main() {%0D%0A    return 0%0D%0A}", lang
            )

        def test_java(self):
            lang = 'java'
            graph_test_models(
                "class Main {%0D%0A    public static void main() {%0D%0A        int a = 0;%0D%0A" +
                "        int b = 2;%0D%0A        a += b;%0D%0A    }%0D%0A}",
                "class Main {%0D%0A    public static void main() {%0D%0A        int a;%0D%0A}", lang
            )

        def test_js(self):
            lang = 'js'
            graph_test_models(
                "<script>%0D%0Avar a = 0;%0D%0Avar b = 2;%0D%0Aa += b;%0D%0A</script>",
                "a = 0;", lang
            )
