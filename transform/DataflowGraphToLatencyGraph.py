from pipeline.LatencyGraph import LatencyGraph

def dataflowGraphToLatencyGraph(dg, sg, eMap):
    lg = LatencyGraph()
    for v_DG in dg.V:
        lg.addVertex(v_DG.name)
    for e_DG in dg.E:
        lat = eMap[e_DG].w
        if len(e_DG.es_mg_sd) > 0:
            srcName_sd = dg.V[e_DG.srcIdx].name
            dstName_sd = dg.V[e_DG.dstIdx].name
            w_sd = sum([e_mg.width for e_mg in e_DG.es_mg_sd])
            comp_sd = [e_mg.name for e_mg in e_DG.es_mg_sd]
            lg.addEdge(comp_sd, srcName_sd, dstName_sd, w_sd, lat, 0)
        if len(e_DG.es_mg_ds) > 0:
            srcName_ds = dg.V[e_DG.dstIdx].name
            dstName_ds = dg.V[e_DG.srcIdx].name
            w_ds = sum([e_mg.width for e_mg in e_DG.es_mg_ds])
            comp_ds = [e_mg.name for e_mg in e_DG.es_mg_ds]
            lg.addEdge(comp_ds, srcName_ds, dstName_ds, w_ds, lat, 0)
    return lg
