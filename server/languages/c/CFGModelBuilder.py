from .AbstractModelBuilder import _AbstractModelBuilder
from ..ModelBuilder import Model


class CFGModelBuilder(_AbstractModelBuilder):
    def __init__(self) -> None:
        super().__init__(Model.CFG)