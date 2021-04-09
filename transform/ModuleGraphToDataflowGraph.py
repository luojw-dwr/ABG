from frontend.ModuleGraph import *
from floorplan.DataflowGraph import *

import numpy as np

def moduleGraphToDataflowGraph(mg):
    V_DG = [DataflowVertex(v) for v in mg.V]
    v_mg2idx = {v_mg : idx for (idx, v_mg) in enumerate(mg.V)}
    E_DG_sd_as_dict = dict()
    E_DG_ds_as_dict = dict()
    w_DG_as_dict = dict()
    for e_mg in mg.E:
        e_dg_srcIdx = v_mg2idx[mg.V_dict[e_mg.instance_read_name]]
        e_dg_dstIdx = v_mg2idx[mg.V_dict[e_mg.instance_write_name]]
        if e_dg_srcIdx < e_dg_dstIdx:
            e_dg_sdIdx = (e_dg_srcIdx, e_dg_dstIdx)
            e_DG_sd = E_DG_sd_as_dict.get(e_dg_sdIdx, [])
            e_DG_sd.append(e_mg)
            e_DG_sd_as_dict[e_dg_sdIdx] = e_DG_sd
            e_DG_ds = E_DG_ds_as_dict.get(e_dg_sdIdx, [])
            E_DG_ds_as_dict[e_dg_sdIdx] = e_DG_ds
            w_DG_as_dict[e_dg_sdIdx] = w_DG_as_dict.get(e_dg_sdIdx, 0) + e_mg.width
        else:
            e_dg_sdIdx = (e_dg_dstIdx, e_dg_srcIdx)
            e_DG_sd = E_DG_sd_as_dict.get(e_dg_sdIdx, [])
            E_DG_sd_as_dict[e_dg_sdIdx] = e_DG_sd
            e_DG_ds = E_DG_ds_as_dict.get(e_dg_sdIdx, [])
            e_DG_ds.append(e_mg)
            E_DG_ds_as_dict[e_dg_sdIdx] = e_DG_ds
            w_DG_as_dict[e_dg_sdIdx] = w_DG_as_dict.get(e_dg_sdIdx, 0) + e_mg.width
    E_DG = [
        DataflowEdge(
            k[0], k[1],
            E_DG_sd_as_dict[k],
            E_DG_ds_as_dict[k],
            w_DG_as_dict[k]
        )
        for k in w_DG_as_dict.keys()
    ]
    return DataflowGraph(V_DG, E_DG)
