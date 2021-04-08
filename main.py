from frontend.ParseV import *
from frontend.ParseCSV import *
from transform.ModuleGraphToDataflowRepresentation import *
from transform.GridGraphToSlotRepresentation import *
from floorplan.abgE import abgE

import numpy as np

vhandle, mg = parseTopV("assets/kernel3_u250/")
gg = parseGridCSV("assets/floorplan/U250.csv")

dfr = moduleGraphToDataflowRepresentation(mg)
sr = gridGraphToSlotRepresentation(gg)

PhiE, PhiV = abgE(dfr.n_DG, sr.n_SG, dfr.As_DG, sr.As_SG, dfr.W_DG, sr.W_SG, 0.85 * np.ones(sr.n_SG))

np.savetxt("build/PhiE.csv", PhiE, fmt="%d")
np.savetxt("build/PhiV.csv", PhiV, fmt="%d")

vhandle.toCustomizedNames()
top_module_name, rtl = vhandle.toRTL()
with open(f"build/{top_module_name}.v", 'w') as f:
    f.write(rtl)
