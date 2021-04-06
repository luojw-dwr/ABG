from frontend.GridGraph import *
from floorplan.SlotRepresentation import *

import numpy as np

def gridGraphToSlotRepresentation(gg):
    V = gg.V
    V_dict = gg.V_dict
    A = sorted(V[-1].area.keys())
    n_SG = len(V)
    vertex2idx = {v : idx for (idx, v) in enumerate(V)}
    As_SG = np.zeros((len(A), n_SG), dtype=np.int)
    W_SG = np.zeros((n_SG, n_SG), dtype=np.int)
    for (idx_k, k) in enumerate(A):
        for (idx_v, v) in enumerate(V):
            As_SG[idx_k, idx_v] = v.area[k]
    for i in range(n_SG):
        for j in range(i):
            W_SG[i, j] = np.abs(V[i].X - V[j].X) + np.abs(V[i].Y - V[j].Y)
    W_SG += W_SG.T
    return SlotRepresentation(V, A, As_SG, W_SG)

