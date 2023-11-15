# Generated from C:/Users/valer/PycharmProjects/GraphViewer/server/kotlin/dot_gen\Tree.g4 by ANTLR 4.10.1
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,4,40,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,
        6,7,6,1,0,1,0,1,1,1,1,1,2,1,2,1,3,1,3,1,4,1,4,1,5,1,5,1,5,5,5,29,
        8,5,10,5,12,5,32,9,5,1,6,4,6,35,8,6,11,6,12,6,36,1,6,1,6,0,0,7,1,
        1,3,2,5,0,7,0,9,0,11,3,13,4,1,0,3,2,0,65,90,97,122,6,0,33,39,42,
        47,58,64,91,93,95,95,123,125,3,0,9,10,13,13,32,32,40,0,1,1,0,0,0,
        0,3,1,0,0,0,0,11,1,0,0,0,0,13,1,0,0,0,1,15,1,0,0,0,3,17,1,0,0,0,
        5,19,1,0,0,0,7,21,1,0,0,0,9,23,1,0,0,0,11,30,1,0,0,0,13,34,1,0,0,
        0,15,16,5,40,0,0,16,2,1,0,0,0,17,18,5,41,0,0,18,4,1,0,0,0,19,20,
        2,48,57,0,20,6,1,0,0,0,21,22,7,0,0,0,22,8,1,0,0,0,23,24,7,1,0,0,
        24,10,1,0,0,0,25,29,3,7,3,0,26,29,3,9,4,0,27,29,3,5,2,0,28,25,1,
        0,0,0,28,26,1,0,0,0,28,27,1,0,0,0,29,32,1,0,0,0,30,28,1,0,0,0,30,
        31,1,0,0,0,31,12,1,0,0,0,32,30,1,0,0,0,33,35,7,2,0,0,34,33,1,0,0,
        0,35,36,1,0,0,0,36,34,1,0,0,0,36,37,1,0,0,0,37,38,1,0,0,0,38,39,
        6,6,0,0,39,14,1,0,0,0,4,0,28,30,36,1,1,6,0
    ]

class TreeLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    WORD = 3
    WS = 4

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'('", "')'" ]

    symbolicNames = [ "<INVALID>",
            "WORD", "WS" ]

    ruleNames = [ "T__0", "T__1", "NUM", "CHAR", "SPECIALS", "WORD", "WS" ]

    grammarFileName = "Tree.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.10.1")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
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


    def action(self, localctx:RuleContext, ruleIndex:int, actionIndex:int):
        if self._actions is None:
            actions = dict()
            actions[6] = self.WS_action 
            self._actions = actions
        action = self._actions.get(ruleIndex, None)
        if action is not None:
            action(localctx, actionIndex)
        else:
            raise Exception("No registered action for:" + str(ruleIndex))


    def WS_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 0:
             self.skip(); 
     


