from ..ModelBuilder import Model
from .AbstractModelBuilder import _AbstractModelBuilder

class CFGModelBuilder(_AbstractModelBuilder):
    def __init__(self) -> None:
        super().__init__(Model.CFG)