import re

from antlr4 import *
from .antlr.Java8Lexer import Java8Lexer
from .antlr.Java8Parser import Java8Parser

from ..ast_view.ast import MyErrorListener, Ast

from ..ModelBuilder import ModelBuilder


class ASTModelBuilder(ModelBuilder):

    def build(self, code: str) -> str:
        inp_stream = InputStream(code)
        lexer = Java8Lexer(inp_stream)
        lexer.removeErrorListeners()
        my_listener = MyErrorListener()
        lexer.addErrorListener(my_listener)
        stream = CommonTokenStream(lexer)
        parser = Java8Parser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(my_listener)
        tree = parser.compilationUnit()

        my_tree = Ast(Java8Parser)
        my_tree.gen_ast(tree, False, 0)
        my_tree.create_dot()
        res = my_tree.dot_tree
        if res == "digraph g {" or res == "digraph g {\n}":
            raise RuntimeError('Something wrong')
        return res


def replace(regex, string, replacement):
    reg = re.compile(regex)
    return reg.sub(replacement, string)
