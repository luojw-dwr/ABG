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
    def withVirtualSS(self):
        lg = LatencyGraph()
        lg.V = self.V.copy()
        lg.Vdict = self.Vdict.copy()
        lg.E = self.E.copy()
        lg.Edict = self.Edict.copy()
        lg.addVertex("__virt_source__")
        lg.addVertex("__virt_sink__")
        for (vIdx, v) in enumerate(self.V):
            isSource = (len(v.sourceNames) == 0)
            isSink = (len(v.sinkNames) == 0)
            if isSource or isSink:
                v_alt = LatencyVertex(v.name)
                lg.V[vIdx] = v_alt
                lg.Vdict[v.name] = v_alt
                if isSource:
                    v_alt.sourceNames = v.sourceNames.copy()
                    lg.addEdge([], "__virt_source__", v.name, 0, 0, 0)
                else:
                    v_alt.sourceNames = v.sourceNames
                if isSink:
                    v_alt.sinkNames = v.sinkNames.copy()
                    lg.addEdge([], v.name, "__virt_sink__", 0, 0, 0)
                else:
                    v_alt.sinkNames = v.sinkNames
        return lg
    def pathsBetween(self, srcName, sinkName, mem):
        if srcName in mem and sinkName in mem[srcName]:
            return mem[srcName][sinkName]
        if srcName == sinkName:
            ret = True, [deque()]
        else:
            ret_paths = deque()
            def extendLeft(xs, x):
                ys = xs.copy()
                ys.appendleft(x)
                return ys
            for nodeName in self.Vdict[srcName].sinkNames:
                reached, paths = self.pathsBetween(nodeName, sinkName, mem)
                if reached:
                    ret_paths.extend([extendLeft(path, self.Edict[(srcName, nodeName)]) for path in paths])
            ret = (len(ret_paths) > 0), ret_paths
        mem[srcName][sinkName] = ret
        return ret
    def reconvergentPathsToVirtSink(self):
        lg = self.withVirtualSS()
        mem = defaultdict(lambda:defaultdict(lambda:None))
        reached, paths = lg.pathsBetween("__virt_source__", "__virt_sink__", mem)
        return [mem[vName]["__virt_sink__"] for vName in self.Vdict]
