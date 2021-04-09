class DataflowVertex:
    def __init__(self, v_mg):
        self.v_mg = v_mg
    def __repr__(self):
        return f"DataflowVertex(v_mg={self.v_mg})"

class DataflowEdge:
    def __init__(self, srcIdx, dstIdx, es_mg_sd, es_mg_ds, w):
        self.srcIdx = srcIdx
        self.dstIdx = dstIdx
        self.es_mg_sd = es_mg_sd
        self.es_mg_ds = es_mg_ds
        self.w = w
    def __repr__(self):
        return f"DataflowEdge(srcIdx={self.srcIdx}, dstIdx={self.dstIdx}, es_mg_sd={self.es_mg_sd}, es_mg_ds={self.es_mg_ds}, w={self.w})"

class DataflowGraph:
    def __init__(self, V, E):
        self.V = V
        self.V_dict = {v.v_mg.instance_name : v for v in self.V}
        self.E = E
    def __repr__(self):
        return f"DataflowGraph(V={self.V}, E={self.E})"
