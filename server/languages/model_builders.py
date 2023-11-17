from .ModelBuilder import *
from .c.model_builders import model_builders as c_model_builders
from .java.model_builders import model_builders as java_model_builders
from .kotlin.model_builders import model_builders as kotlin_model_builders
from .go.model_builders import model_builders as go_model_builders
from .python.model_builders import model_builders as python_model_builders
from .js.model_builders import model_builders as js_model_builders

model_builders = {
    Language.C: c_model_builders,
    Language.JAVA: java_model_builders,
    Language.KOTLIN: kotlin_model_builders,
    Language.GO: go_model_builders,
    Language.PYTHON: python_model_builders,
    Language.JS: js_model_builders
}


def get_model_builder(lang: str, model: str) -> ModelBuilder | None:
    try:
        return model_builders[Language(lang.lower())][Model(model.lower())]
    except Exception:
        return None
