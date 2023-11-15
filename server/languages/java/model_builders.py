from ..ModelBuilder import Model
from .ASTModelBuilder import ASTModelBuilder
from .CFGModelBuilder import CFGModelBuilder

model_builders = {
    Model.AST: ASTModelBuilder(),
    Model.CFG: CFGModelBuilder()
}
