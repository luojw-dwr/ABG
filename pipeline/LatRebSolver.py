import numpy as np
import gurobipy as gp
from gurobipy import GRB

class LatRebSolver:
    def __init__(self, lg):
        self.lg = lg
    def solve(self):
        lg = self.lg
        lg.V = list(lg.V)
        lg.E = list(lg.E)
        nV_LG = len(lg.V)
        v2idx = {v : vIdx for (vIdx, v) in enumerate(lg.V)}
        L = np.zeros((nV_LG, nV_LG), dtype=np.int)
        W = np.zeros((nV_LG, nV_LG), dtype=np.int)
        for e_LG in lg.E:
            srcIdx = v2idx[lg.Vdict[e_LG.srcName]]
            dstIdx = v2idx[lg.Vdict[e_LG.dstName]]
            L[srcIdx, dstIdx] = e_LG.lat
            W[srcIdx, dstIdx] = e_LG.w
        m = gp.Model("LatReb")
        S = m.addMVar((nV_LG, 1), name="S")
        B = m.addMVar((nV_LG, nV_LG), name="B")
        m.update()
        for vIdx in range(nV_LG):
            m.addConstr(S[vIdx] >= 0)
        for e_LG in lg.E:
            srcIdx = v2idx[lg.Vdict[e_LG.srcName]]
            dstIdx = v2idx[lg.Vdict[e_LG.dstName]]
            m.addConstr(B[srcIdx, dstIdx] == S[srcIdx, 0] - S[dstIdx, 0] - L[srcIdx, dstIdx])
            m.addConstr(B[srcIdx, dstIdx] >= 0)
        loss = sum([
            W[i, j] * B[i, j]
            for j in range(nV_LG)
            for i in range(nV_LG)
        ])
        m.setObjective(loss, GRB.MINIMIZE)
        m.optimize()
        solution = np.array(m.getAttr("X"), dtype=np.int)
        solution_S = solution[:nV_LG]
        solution_B = solution[nV_LG:].reshape((nV_LG, nV_LG))
        return solution_S, solution_B
