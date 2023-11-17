# Generated from C:/Users/valer/PycharmProjects/GraphViewer/server/kotlin/dot_gen\Tree.g4 by ANTLR 4.10.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,4,30,2,0,7,0,2,1,7,1,2,2,7,2,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,
        1,1,5,1,16,8,1,10,1,12,1,19,9,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,3,2,
        28,8,2,1,2,0,0,3,0,2,4,0,0,28,0,6,1,0,0,0,2,10,1,0,0,0,4,27,1,0,
        0,0,6,7,5,1,0,0,7,8,3,2,1,0,8,9,5,2,0,0,9,1,1,0,0,0,10,11,5,3,0,
        0,11,17,6,1,-1,0,12,13,3,4,2,0,13,14,6,1,-1,0,14,16,1,0,0,0,15,12,
        1,0,0,0,16,19,1,0,0,0,17,15,1,0,0,0,17,18,1,0,0,0,18,3,1,0,0,0,19,
        17,1,0,0,0,20,21,5,3,0,0,21,28,6,2,-1,0,22,23,5,1,0,0,23,24,3,2,
        1,0,24,25,5,2,0,0,25,26,6,2,-1,0,26,28,1,0,0,0,27,20,1,0,0,0,27,
        22,1,0,0,0,28,5,1,0,0,0,2,17,27
    ]

class TreeParser ( Parser ):

    grammarFileName = "Tree.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "WORD", "WS" ]

    RULE_tree_def = 0
    RULE_tree_form = 1
    RULE_subnode = 2

    ruleNames =  [ "tree_def", "tree_form", "subnode" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    WORD=3
    WS=4

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.10.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    node_list   = []
    connections = []
    node_count  = 0

    def add_node(self, name):
        self.node_count += 1
        internal_name = "Node" + str(self.node_count)
        # print "Adding node", (internal_name, name)
        self.node_list.append((internal_name, '"' + name + '"'))
        return internal_name

    def connect(self, node1, node2):
        # print "Connection", node1, "->", node2
        self.connections.append( (node1, node2) )



    class Tree_defContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def tree_form(self):
            return self.getTypedRuleContext(TreeParser.Tree_formContext,0)


        def getRuleIndex(self):
            return TreeParser.RULE_tree_def

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTree_def" ):
                listener.enterTree_def(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTree_def" ):
                listener.exitTree_def(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTree_def" ):
                return visitor.visitTree_def(self)
            else:
                return visitor.visitChildren(self)




    def tree_def(self):

        localctx = TreeParser.Tree_defContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_tree_def)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 6
            self.match(TreeParser.T__0)
            self.state = 7
            self.tree_form()
            self.state = 8
            self.match(TreeParser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Tree_formContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.head = ""
            self.a = None # Token
            self.b = None # SubnodeContext

        def WORD(self):
            return self.getToken(TreeParser.WORD, 0)

        def subnode(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TreeParser.SubnodeContext)
            else:
                return self.getTypedRuleContext(TreeParser.SubnodeContext,i)


        def getRuleIndex(self):
            return TreeParser.RULE_tree_form

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTree_form" ):
                listener.enterTree_form(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTree_form" ):
                listener.exitTree_form(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTree_form" ):
                return visitor.visitTree_form(self)
            else:
                return visitor.visitChildren(self)




    def tree_form(self):

        localctx = TreeParser.Tree_formContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_tree_form)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 10
            localctx.a = self.match(TreeParser.WORD)
            localctx.head = self.add_node((None if localctx.a is None else localctx.a.text))
            self.state = 17
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==TreeParser.T__0 or _la==TreeParser.WORD:
                self.state = 12
                localctx.b = self.subnode()
                self.connect(localctx.head, localctx.b.node_name) 
                self.state = 19
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SubnodeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.node_name = None
            self.b = None # Token
            self._tree_form = None # Tree_formContext

        def WORD(self):
            return self.getToken(TreeParser.WORD, 0)

        def tree_form(self):
            return self.getTypedRuleContext(TreeParser.Tree_formContext,0)


        def getRuleIndex(self):
            return TreeParser.RULE_subnode

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSubnode" ):
                listener.enterSubnode(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSubnode" ):
                listener.exitSubnode(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSubnode" ):
                return visitor.visitSubnode(self)
            else:
                return visitor.visitChildren(self)




    def subnode(self):

        localctx = TreeParser.SubnodeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_subnode)
        try:
            self.state = 27
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [TreeParser.WORD]:
                self.enterOuterAlt(localctx, 1)
                self.state = 20
                localctx.b = self.match(TreeParser.WORD)
                localctx.node_name = self.add_node((None if localctx.b is None else localctx.b.text)) 
                pass
            elif token in [TreeParser.T__0]:
                self.enterOuterAlt(localctx, 2)
                self.state = 22
                self.match(TreeParser.T__0)
                self.state = 23
                localctx._tree_form = self.tree_form()
                self.state = 24
                self.match(TreeParser.T__1)
                localctx.node_name = localctx._tree_form.head 
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





