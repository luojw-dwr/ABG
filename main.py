from frontend.ParseV import *
from frontend.ParseCSV import *
from transform.ModuleGraphToDataflowGraph import *
from transform.GridGraphToSlotGraph import *
from floorplan.AbgESolver import AbgESolver
from transform.DataflowGraphToLatencyGraph import *

import numpy as np

from collections import defaultdict

import logging
logger = logging.getLogger("ABG_main")
logger.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
logHandler.setFormatter(logging.Formatter(logging.BASIC_FORMAT, None))
logger.addHandler(logHandler)

logger.info("[Op Phase] Parse assets.")
vhandle, mg = parseTopV("assets/kernel3_u250/")
gg = parseGridCSV("assets/floorplan/U250.csv")

logger.info("[Op Phase] Construct AbgE problem.")
dg = moduleGraphToDataflowGraph(mg)
sg = gridGraphToSlotGraph(gg)
abgESolver = AbgESolver(dg, sg, defaultdict(lambda:0.85), None)

logger.info("[Op Phase] Solve AbgE problem.")
PhiV, PhiE = abgESolver.solve()
vMap, eMap = abgESolver.resolveMap(PhiV, PhiE)

logger.info("[Op Phase] Resolve reconvergent paths.")
lg_raw = dataflowGraphToLatencyGraph(dg, sg, eMap)
rps = lg_raw.reconvergentPathsToVirtSink()
#logger.info("[Op Phase] Construct LatRebal problem.")

logger.info("[Op Phase] Generate optimized RTL.")
vhandle.toCustomizedNames()
top_module_name, rtl = vhandle.toRTL()

logger.info("[Op Phase] Store optimized RTL.")
with open(f"build/{top_module_name}.v", 'w') as f:
    f.write(rtl)
