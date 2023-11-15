from staticfg import CFGBuilder
from uuid import uuid4 as uuid
import os

from ..ModelBuilder import ModelBuilder

class CFGModelBuilder(ModelBuilder):
    
    def build(self, code: str) -> str:
        cfg = CFGBuilder().build_from_src(name='test', src=code)
        # cfg.draw('out.png', prog='dot')
        filename = str(uuid().hex)
        cfg.build_visual(filename, 'dot', show=False)

        text = open(filename).read()
        os.remove(filename)
        os.remove(filename + '.dot')
        return text