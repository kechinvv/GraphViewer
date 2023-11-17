from antlr4 import *
from .antlr.KotlinLexer import KotlinLexer
from .antlr.KotlinParser import KotlinParser

from ..ast_view.ast import Ast, MyErrorListener
from ..ModelBuilder import ModelBuilder


class ASTModelBuilder(ModelBuilder):

    def build(self, code: str) -> str:
        inp_stream = InputStream(code)
        lexer = KotlinLexer(inp_stream)
        lexer.removeErrorListeners()
        my_listener = MyErrorListener()
        lexer.addErrorListener(my_listener)
        stream = CommonTokenStream(lexer)
        parser = KotlinParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(my_listener)
        tree = parser.kotlinFile()
        # str_tree = Trees.toStringTree(tree, None, parser)
        # reg = re.compile(r'\s\(\s*\)')
        # sub = reg.sub('', str_tree)
        # sub = str_tree.replace('"', '\\"')
        # print(sub)
        # return get_dot(sub)
        my_tree = Ast(KotlinParser)
        my_tree.gen_ast(tree, False, 0)
        my_tree.create_dot()
        res = my_tree.dot_tree
        if res == "digraph g {" or res == "digraph g {\n}":
            raise RuntimeError('Something wrong')
        return res
