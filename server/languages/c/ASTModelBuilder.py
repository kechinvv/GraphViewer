from antlr4 import *
from .antlr.CLexer import CLexer
from .antlr.CParser import CParser

from ..ast_view.ast import Ast, MyErrorListener

from ..ModelBuilder import ModelBuilder


class ASTModelBuilder(ModelBuilder):
    def build(self, code: str) -> str:
        inp_stream = InputStream(code)
        lexer = CLexer(inp_stream)
        lexer.removeErrorListeners()
        my_listener = MyErrorListener()
        lexer.addErrorListener(my_listener)
        stream = CommonTokenStream(lexer)
        parser = CParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(my_listener)
        tree = parser.compilationUnit()
        my_tree = Ast(CParser)
        my_tree.gen_ast(tree, False, 0)
        my_tree.create_dot()
        res = my_tree.dot_tree
        if res == "digraph g {" or res == "digraph g {\n}":
            raise RuntimeError('Something wrong')
        return res
