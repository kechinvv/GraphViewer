from ..ModelBuilder import Model
from .AbstractModelBuilder import _AbstractModelBuilder


class ASTModelBuilder(_AbstractModelBuilder):
    def __init__(self) -> None:
        super().__init__(Model.AST)
