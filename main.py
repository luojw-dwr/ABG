import logging
logger = logging.getLogger("ABG_main")
logger.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
logHandler.setFormatter(logging.Formatter(logging.BASIC_FORMAT, None))
logger.addHandler(logHandler)

from frontend.ParseV import *
from frontend.ParseCSV import *
from transform.ModuleGraphToDataflowGraph import *
from transform.GridGraphToSlotGraph import *
from floorplan.AbgESolver import AbgESolver
from transform.DataflowGraphToLatencyGraph import *
from pipeline.LatRebSolver import LatRebSolver
from backend.LatencyGraphToBufferSpec import *

import numpy as np

from collections import defaultdict

import yaml

import os
def execAndEcho(cmd):
    logger.info(f"[os.system] {cmd}")
    os.system(cmd)


logger.info("[Op Phase] Generate build file system.")
output_dirs = [
    "build/",
    "build/csv/",
    "build/tcl/",
    "build/verilog/",
    "build/yaml/",
]
for dir in output_dirs:
    try:
        os.makedirs(dir)
    except FileExistsError:
        pass

logger.info("[Op Phase] Parse assets.")
path_hlsproj          = "assets/kernel3_u250"
path_prefloorplan_tcl = "assets/floorplan/U250.tcl"
path_prefloorplan_csv = "assets/floorplan/U250.csv"
logger.info(f"[Param] path_hlsproj={path_hlsproj}")
logger.info(f"[Param] path_prefloorplan_tcl={path_prefloorplan_tcl}")
logger.info(f"[Param] path_prefloorplan_csv={path_prefloorplan_csv}")
vhandle, mg = parseTopV(path_hlsproj)
gg = parseGridCSV(path_prefloorplan_csv)

logger.info("[Op Phase] Construct AbgE problem.")
dg = moduleGraphToDataflowGraph(mg)
sg = gridGraphToSlotGraph(gg)
abgESolver = AbgESolver(dg, sg, defaultdict(lambda:0.85), None)

logger.info("[Op Phase] Solve AbgE problem.")
PhiV, PhiE = abgESolver.solve()
vMap, eMap = abgESolver.resolveMap(PhiV, PhiE)

with open("build/yaml/AbgE_vMap.yaml", 'w') as f:
    yaml.dump({
        v_DG.name : v_SG.name
        for (v_DG, v_SG) in vMap.items()
    }, f)
with open("build/yaml/AbgE_eMap.yaml", 'w') as f:
    yaml.dump({
        (dg.V[e_DG.srcIdx].name, dg.V[e_DG.dstIdx].name) : (sg.V[e_SG.srcIdx].name, sg.V[e_SG.dstIdx].name)
        for (e_DG, e_SG) in eMap.items()
    }, f)

logger.info("[Op Phase] Construct LatReb problem.")
lg_raw = dataflowGraphToLatencyGraph(dg, sg, eMap)
latRebSolver = LatRebSolver(lg_raw)
logger.info("[Op Phase] Solve LatReb problem.")
S, B = latRebSolver.solve()
lg_bal = latRebSolver.resolveBal(S, B)

logger.info("[Op Phase] Store LatReb solution.")
with open("build/yaml/LatReb_vLat.yaml", 'w') as f:
    yaml.dump({
        v_LG.name : int(v_LG.lat)
        for v_LG in lg_bal.V
    }, f)
with open("build/yaml/LatReb_eLatBal.yaml", 'w') as f:
    yaml.dump({
        e_MG.name : {"lat": int(e_LG.lat), "bal": int(e_LG.bal)}
        for e_LG in lg_bal.E
        for e_MG in e_LG.components
    }, f)

logger.info("[Op Phase] Generate optimized top RTL.")
vhandle.toCustomizedNames()
top_module_name, rtl = vhandle.toRTL()

logger.info("[Op Phase] Store optimized top RTL.")
with open(f"build/verilog/{top_module_name}.v", 'w') as f:
    f.write(rtl)

logger.info("[Op Phase] Generate cross-die buffer specifications.")
buffer_specs = latencyGraphToBufferSpec(lg_bal)

logger.info("[Op Phase] Store cross-die buffer specifications.")
with open(f"build/csv/bufferspecs.csv", 'w') as f:
    f.write(buffer_specs)

logger.info("[Op Phase] Generate cross-die buffer RTLs.")
execAndEcho("cp build/csv/bufferspecs.csv chisel3/bvhlsfifo/hw/req.csv")
execAndEcho("make -C chisel3/bvhlsfifo/")

logger.info("[Op Phase] Store cross-die buffer RTLs.")
execAndEcho("cp chisel3/bvhlsfifo/builds/*.v build/verilog/")

logger.info("[Op Phase] Copy coarse pre-floorplan constraint.")
execAndEcho(f"cp {path_prefloorplan_tcl} build/tcl/prefloorplan.tcl")

logger.info("[Op Phase] Generate PE floorplan constraints.")

logger.info("[Op Phase] Store PE floorplan constraints.")

logger.info("[Op Phase] Generate cross-die buffer floorplan constraints.")

logger.info("[Op Phase] Store cross-die buffer floorplan constraints.")
