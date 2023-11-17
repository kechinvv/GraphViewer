from enum import Enum


class ModelBuilder:
    def build(self, code: str) -> str:
        pass


class Language(Enum):
    C = "c"
    JAVA = "java"
    KOTLIN = "kotlin"
    GO = "go"
    PYTHON = "python"
    JS = "js"


class Model(Enum):
    AST = "ast"
    CFG = "cfg"
    SSA = "ssa"
