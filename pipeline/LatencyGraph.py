from collections import deque
from collections import defaultdict
from copy import deepcopy

class LatencyEdge:
    def __init__(self, components, srcName, dstName, w, lat, bal):
        self.components = components
        self.srcName = srcName
        self.dstName = dstName
        self.w = w
        self.lat = lat
        self.bal = bal
    def __repr__(self):
        return f"LatencyEdge(components={self.components}, srcName={self.srcName}, dstName={self.dstName}, w={self.w}, lat={self.lat}, bal={self.bal})"

class LatencyVertex:
    def __init__(self, name):
        self.name = name
        self.sourceNames = deque()
        self.sinkNames = deque()
    def __repr__(self):
        return f"LatencyVertex(name={self.name}, sourceNames={self.sourceNames}, sinkNames={self.sinkNames})"

class LatencyGraph:
    def __init__(self):
        self.V = deque()
        self.Vdict = {}
        self.E = deque()
        self.Edict = {}
    def __repr__(self):
        return f"LatencyGraph(V={self.V}, E={self.E})"
    def addVertex(self, name):
        v = LatencyVertex(name)
        self.V.append(v)
        self.Vdict[name] = v
    def addEdge(self, comp, srcName, dstName, w, lat, bal):
        e = LatencyEdge(comp, srcName, dstName, w, lat, bal)
        self.E.append(e)
        self.Edict[(srcName, dstName)] = e
        self.Vdict[srcName].sinkNames.append(dstName)
        self.Vdict[dstName].sourceNames.append(srcName)
