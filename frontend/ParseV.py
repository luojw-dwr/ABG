import os
import sys
sys.setrecursionlimit(100000)
from collections import deque, defaultdict

import re

import pyverilog.vparser.ast as vast
from pyverilog.vparser.parser import parse as vparse

from xml.dom import minidom
from xml.dom.minidom import parse as xparse

from .ModuleGraph import *

def do_dfs(node, visited, f):
    if (node not in visited):
        visited.add(node)
    else:
        return
    f(node)
    for c in node.children():
        do_dfs(c, visited, f)

def dfs(node, f):
    do_dfs(node, set(), f)

def mkParallel(f, g):
    def h(x):
        f(x), g(x)
    return h

def parsePE(path_proj, name_top, vnode):
    name_pe = vnode.module[len(name_top)+1:]
    func_name = vnode.module[len(name_top)+1:]
    module_name = vnode.module
    instance_name = vnode.name
    if "axi" in name_pe:
        area_dict = defaultdict(int)
    else:
        path_rpt = os.path.join(path_proj, "solution/syn/report/")
        path_xml = os.path.join(path_rpt, f"{name_pe}_csynth.xml")
        xnode_root = xparse(path_xml)
        xnode_Resources = xnode_root.getElementsByTagName("Resources")[0]
        area_dict = dict()
        for xnode_r in xnode_Resources.childNodes:
            if xnode_r.nodeType == minidom.Node.ELEMENT_NODE:
                k = xnode_r.nodeName.upper()
                v = int(xnode_r.firstChild.nodeValue)
                area_dict[k] = v
    return ModuleVertex(func_name, module_name, instance_name, area_dict)

def parseFIFO(path_proj, name_top, vnode):
    module_name = vnode.module
    instance_name = vnode.name
    width, depth = 0, 0
    for field in vnode.module.split("_"):
        if field[0] == 'w':
            width = int(field[1:])
        elif field[0] == 'd':
            depth = int(field[1:])
    instance_read_name, instance_write_name = "", ""
    for vnode_port in vnode.portlist:
        if vnode_port.portname == "if_read":
            instance_read_name = re.match("[a-zA-Z_0-9]*_U[0-9]*", vnode_port.argname.name).group()
        elif vnode_port.portname == "if_write":
            instance_write_name = re.match("[a-zA-Z_0-9]*_U[0-9]*", vnode_port.argname.name).group()
    return ModuleEdge(module_name, instance_name, width, depth, instance_read_name, instance_write_name)

def parseTopV(path_proj, name_top):
    path_src = os.path.join(path_proj, "solution/syn/verilog/")
    path_top = os.path.join(path_src, f"{name_top}_{name_top}.v")
    ast, directives = vparse((path_top,))
    def gen_collectFIFO(name_top, lst):
        prefix_fifo = f"{name_top}_fifo"
        def collectFIFO(node):
            if isinstance(node, vast.Instance) and node.module.startswith(prefix_fifo):
                lst.append(node)
        return collectFIFO
    def gen_collectPE(name_top, lst):
        prefix_fifo = f"{name_top}_fifo"
        def collectPE(node):
            if isinstance(node, vast.Instance) and (not node.module.startswith(prefix_fifo)):
                lst.append(node)
        return collectPE
    vnodes_pe, vnodes_fifo = deque(), deque()
    dfs(ast,
        mkParallel(
            gen_collectPE(name_top, vnodes_pe),
            gen_collectFIFO(name_top, vnodes_fifo)))
    mnodes = [parsePE(path_proj, name_top, vnode_pe) for vnode_pe in vnodes_pe]
    medges = [parseFIFO(path_proj, name_top, vnode_fifo) for vnode_fifo in vnodes_fifo]
    return ModuleGraph(V=mnodes, E=medges)

