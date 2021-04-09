class DataflowVertex:
    def __init__(self, v_mg):
        self.v_mg = v_mg
    def __repr__(self):
        return f"DataflowVertex(v_mg={self.v_mg})"

class DataflowEdge:
    def __init__(self, src, dst, es_mg_sd, es_mg_ds, w):
        self.src = src
        self.dst = dst
        self.es_mg_sd = es_mg_sd
        self.es_mg_ds = es_mg_ds
        self.w = w
    def __repr__(self):
        return f"DataflowEdge(src={self.src}, dst={self.dst}, es_mg_sd={self.es_mg_sd}, es_mg_ds={self.es_mg_ds}, w={self.w})"

class DataflowGraph:
    def __init__(self, V, E):
        self.V = V
        self.E = E
    def __repr__(self):
        return f"DataflowGraph(V={self.V}, E={self.E})"
