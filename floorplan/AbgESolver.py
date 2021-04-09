import numpy as np
import gurobipy as gp
from gurobipy import GRB

class AbgESolver:
    def __init__(self, dg, sg, rho, userConstrGen):
        self.dg = dg
        self.sg = sg
        self.rho = rho
        self.userConstrGen = userConstrGen
    def solve(self):
        dg = self.dg
        sg = self.sg
        rho_SG = np.array([self.rho[v_SG.name] for v_SG in sg.V])
        userConstrGen = self.userConstrGen
        nV_DG = len(dg.V)
        nE_DG = len(dg.E)
        nV_SG = len(sg.V)
        nE_SG = len(sg.E)
        A = sg.V[0].area.keys()
        nA = len(A)
        As_DG = np.zeros((len(A), nV_DG), dtype=np.int)
        As_SG = np.zeros((len(A), nV_SG), dtype=np.int)
        for aIdx, a in enumerate(A):
            for vIdx_DG, v_DG in enumerate(dg.V):
                As_DG[aIdx, vIdx_DG] = v_DG.v_mg.area[a]
            for vIdx_SG, v_SG in enumerate(sg.V):
                As_SG[aIdx, vIdx_SG] = v_SG.area[a]
        w_DG = np.array([e_DG.w for e_DG in dg.E])
        w_SG = np.array([e_SG.w for e_SG in sg.E])
        S_SG = np.zeros((nV_SG, nE_SG), dtype=np.int)
        D_SG = np.zeros((nV_SG, nE_SG), dtype=np.int)
        V_DG = np.eye(nV_DG)
        V_SG = np.eye(nV_SG)
        for eIdx_SG, e_SG in enumerate(sg.E):
            S_SG[:, eIdx_SG] = V_SG[:, e_SG.srcIdx]
            D_SG[:, eIdx_SG] = V_SG[:, e_SG.dstIdx]
        m = gp.Model("abgE")
        PhiV = m.addMVar((nV_SG, nV_DG), name="PhiV", vtype=GRB.BINARY)
        PhiE = m.addMVar((nE_SG, nE_DG), name="PhiE", vtype=GRB.BINARY)
        m.update()
        if userConstrGen:
            m.addConstrs(userConstrGen(dg=dg, sg=sg, m=m, PhiV=PhiV, PhiE=PhiE))
        for i in range(nV_DG):
            m.addConstr(sum(PhiV[:, i]) == 1)
        for i in range(nE_DG):
            m.addConstr(sum(PhiE[:, i]) == 1)
        for eIdx_DG, e_DG in enumerate(dg.E):
            m.addConstr(S_SG @ PhiE[:, eIdx_DG] == PhiV[:, e_DG.srcIdx])
            m.addConstr(D_SG @ PhiE[:, eIdx_DG] == PhiV[:, e_DG.dstIdx])
        for k in range(nA):
            for i in range(nV_SG):
                m.addConstr(As_DG[k].T @ PhiV[i, :] <= np.int(np.round(rho_SG[i] * As_SG[k, i])))
        loss = sum([
            w_DG[eIdx_DG] * (w_SG.T @ PhiE[:, eIdx_DG])
            for eIdx_DG in range(nE_DG)
        ])
        m.setObjective(loss, GRB.MINIMIZE)
        m.optimize()
        solution = np.array(m.getAttr("X"), dtype=np.int)
        solution_PhiV = solution[:(nV_SG * nV_DG)].reshape((nV_SG, nV_DG))
        solution_PhiE = solution[(nV_SG * nV_DG):].reshape((nE_SG, nE_DG))
        return (solution_PhiE, solution_PhiV)
