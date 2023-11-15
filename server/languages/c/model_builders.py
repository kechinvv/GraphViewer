from ..ModelBuilder import Model
from .ASTModelBuilder import ASTModelBuilder
from .CFGModelBuilder import CFGModelBuilder
from .SSAModelBuilder import SSAModelBuilder


model_builders = {
    Model.AST: ASTModelBuilder(),
    Model.CFG: CFGModelBuilder(),
    Model.SSA: SSAModelBuilder()
}
