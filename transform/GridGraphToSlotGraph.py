from frontend.GridGraph import *
from floorplan.SlotGraph import *

import numpy as np

def gridGraphToSlotGraph(gg):
    V_sg = [SlotVertex(v_gg.name, v_gg.area) for v_gg in gg.V]
    v_gg2idx = {v_gg : idx for (idx, v_gg) in enumerate(gg.V)}
    E_sg = [
        SlotEdge(i, j,
            np.abs(gg.V[i].X - gg.V[j].X, dtype=np.int) +
            np.abs(gg.V[i].Y - gg.V[j].Y, dtype=np.int)
        )
        for j in range(len(gg.V))
        for i in range(j + 1)
    ]
    return SlotGraph(V_sg, E_sg)
