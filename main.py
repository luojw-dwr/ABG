from frontend.ParseV import *
from frontend.ParseCSV import *
from transform.ModuleGraphToDataflowRepresentation import *
from transform.GridGraphToSlotRepresentation import *
from floorplan.abgV import abgV
from floorplan.abgE import abgE

import numpy as np

mg = parseTopV("assets/kernel3_u250/", "kernel3")
gg = parseGridCSV("assets/U250.csv")

dfr = moduleGraphToDataflowRepresentation(mg)
sr = gridGraphToSlotRepresentation(gg)

print(dfr)
print(sr)

PhiE, PhiV = abgE(dfr.n_DG, sr.n_SG, dfr.As_DG, sr.As_SG, dfr.W_DG, sr.W_SG, 0.85 * np.ones(sr.n_SG))

np.savetxt("build/PhiE.csv", PhiE, fmt="%d")
np.savetxt("build/PhiV.csv", PhiV, fmt="%d")
