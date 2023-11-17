# Generated from C:/Users/valer/PycharmProjects/GraphViewer/server/kotlin/dot_gen\Tree.g4 by ANTLR 4.10.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .TreeParser import TreeParser
else:
    from TreeParser import TreeParser

# This class defines a complete generic visitor for a parse tree produced by TreeParser.

class TreeVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by TreeParser#tree_def.
    def visitTree_def(self, ctx:TreeParser.Tree_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TreeParser#tree_form.
    def visitTree_form(self, ctx:TreeParser.Tree_formContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TreeParser#subnode.
    def visitSubnode(self, ctx:TreeParser.SubnodeContext):
        return self.visitChildren(ctx)



del TreeParser