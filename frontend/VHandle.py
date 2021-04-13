import pyverilog.vparser.ast as vast
from pyverilog.ast_code_generator.codegen import ASTCodeGenerator as VGen

import sys
sys.setrecursionlimit(100000)

import logging

logger = logging.getLogger("ABG_VHandle")
logger.setLevel(logging.DEBUG)
logHandler = logging.StreamHandler()
logHandler.setFormatter(logging.Formatter(logging.BASIC_FORMAT, None))
logger.addHandler(logHandler)

class VHandle:
    def __init__(self, vnode_root, vnodes_pe, vnodes_fifo, vnodes_fifoInst):
        self.vnode_root      = vnode_root
        self.vnode_moduleDef = vnode_root.children()[0].children()[1]
        self.vnodes_pe       = vnodes_pe
        self.vnodes_fifo     = vnodes_fifo
        self.vnodes_fifoInst = vnodes_fifoInst
    def toCustomizedNames(self):
        logger.debug(f"Original Top Module Name: {self.vnode_moduleDef.name}")
        self.vnode_moduleDef.name += "_postABG"
        logger.debug(f"Modified Top Module Name: {self.vnode_moduleDef.name}")
        for vnode_fifoInst in self.vnodes_fifoInst:
            vnode_fifo = next(filter(lambda node : isinstance(node, vast.Instance), vnode_fifoInst.children()))
            assert(vnode_fifoInst.module == vnode_fifo.module)
            logger.debug(f"Original FIFO Module Name for Instance {vnode_fifo.name}: {vnode_fifo.module}")
            vnode_fifoInst.module = vnode_fifo.name + "_M"
            vnode_fifo.module = vnode_fifo.name + "_M"
            assert(vnode_fifoInst.module == vnode_fifo.module)
            logger.debug(f"Modified FIFO Module Name for Instance {vnode_fifo.name}: {vnode_fifo.module}")
    def toRTL(self):
        # may involve deep recursion...
        # due to impl. of pyverilog ASTCodeGenerator ...
        # which is a recursive DFS
        top_module_name = self.vnode_moduleDef.name
        rtl = VGen().visit(self.vnode_moduleDef)
        return top_module_name, rtl
