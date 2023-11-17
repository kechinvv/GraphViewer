from enum import Enum


class ModelBuilder:
    def build(self, code: str) -> str:
        pass


class Language(Enum):
    C = "c_cpp"
    JAVA = "java"
    KOTLIN = "kotlin"
    GO = "golang"
    PYTHON = "python"
    JS = "javascript"


class Model(Enum):
    AST = "ast"
    CFG = "cfg"
    SSA = "ssa"
