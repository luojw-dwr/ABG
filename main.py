from frontend.ParseV import *
from frontend.ParseCSV import *
from transform.ModuleGraphToDataflowGraph import *
from transform.GridGraphToSlotGraph import *
from floorplan.AbgESolver import AbgESolver

import numpy as np

from collections import defaultdict

vhandle, mg = parseTopV("assets/kernel3_u250/")
gg = parseGridCSV("assets/floorplan/U250.csv")

dg = moduleGraphToDataflowGraph(mg)
sg = gridGraphToSlotGraph(gg)

abgESolver = AbgESolver(dg, sg, defaultdict(lambda:0.85), None)
PhiV, PhiE = abgESolver.solve()
gMap = abgESolver.resolveMap(PhiV, PhiE)
print(gMap)

np.savetxt("build/PhiE.csv", PhiE, fmt="%d")
np.savetxt("build/PhiV.csv", PhiV, fmt="%d")

vhandle.toCustomizedNames()
top_module_name, rtl = vhandle.toRTL()
with open(f"build/{top_module_name}.v", 'w') as f:
    f.write(rtl)
