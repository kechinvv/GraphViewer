from enum import Enum


class ModelBuilder:
    def build(self, code: str) -> str:
        pass


class Language(Enum):
    C_CPP = "c_cpp"
    JAVA = "java"
    KOTLIN = "kotlin"
    GOLANG = "golang"
    PYTHON = "python"
    JAVASCRIPT = "javascript"


class Model(Enum):
    AST = "ast"
    CFG = "cfg"
    SSA = "ssa"
