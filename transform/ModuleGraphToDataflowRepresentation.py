from frontend.ModuleGraph import *
from floorplan.DataflowRepresentation import *

import numpy as np

def moduleGraphToDataflowRepresentation(mg):
    V = mg.V
    V_dict = mg.V_dict
    E = mg.E
    A = sorted(V[-1].area.keys())
    n_DG = len(V)
    vertex2idx = {v : idx for (idx, v) in enumerate(V)}
    As_DG = np.zeros((len(A), n_DG), dtype=np.int)
    W_DG = np.zeros((n_DG, n_DG), dtype=np.int)
    for (idx_k, k) in enumerate(A):
        for (idx_v, v) in enumerate(V):
            As_DG[idx_k, idx_v] = v.area[k]
    for e in E:
        W_DG[vertex2idx[V_dict[e.instance_read_name]], vertex2idx[V_dict[e.instance_write_name]]] += e.width * e.depth
    W_DG += W_DG.T
    return DataflowRepresentation(V, A, As_DG, W_DG)

