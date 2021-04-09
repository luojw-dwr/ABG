class SlotVertex:
    def __init__(self, name, area):
        self.name = name
        self.area = area
    def __repr__(self):
        return f"SlotVertex(name={self.name}, area={self.area})"

class SlotEdge:
    def __init__(self, srcIdx, dstIdx, w):
        self.srcIdx = srcIdx
        self.dstIdx = dstIdx
        self.w = w
    def __repr__(self):
        return f"SlotEdge(srcIdx={self.srcIdx}, dstIdx={self.dstIdx}, w={self.w})"

class SlotGraph:
    def __init__(self, V, E):
        self.V = V
        self.V_dict = {v.name : V for v in V}
        self.E = E
    def __repr__(self):
        return f"SlotGraph(V={self.V}, E={self.E})"
