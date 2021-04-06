import numpy as np
import gurobipy as gp
from gurobipy import GRB

def abgE(nV_DG, nV_SG, As_DG, As_SG, W_DG, W_SG, rho_SG, userConstrsGen=None):
    assert(len(As_DG) == len(As_SG))
    nA = len(As_DG)
    V_DG = np.eye(nV_DG)
    V_SG = np.eye(nV_SG)
    E_DG = np.array([(i, j) for i in range(nV_DG) for j in range(i) if W_DG[i, j] > 0])
    E_SG = np.array([(i, j) for i in range(nV_SG) for j in range(i) if W_SG[i, j] > 0] + [(i, i) for i in range(nV_SG)])
    nE_DG = len(E_DG)
    nE_SG = len(E_SG)
    w_DG = np.array([W_DG[eI_DG, eJ_DG] for (eI_DG, eJ_DG) in E_DG])
    w_SG = np.array([W_SG[eI_SG, eJ_SG] for (eI_SG, eJ_SG) in E_SG])
    S_SG = np.zeros((nV_SG, nE_SG), dtype=np.int)
    D_SG = np.zeros((nV_SG, nE_SG), dtype=np.int)
    for eIdx_SG, (eI_SG, eJ_SG) in enumerate(E_SG):
        S_SG[:, eIdx_SG] = V_SG[:, eI_SG]
        D_SG[:, eIdx_SG] = V_SG[:, eJ_SG]
    m = gp.Model("abrr")
    PhiE = m.addMVar((nE_SG, nE_DG), name="PhiE", vtype=GRB.BINARY)
    PhiV = m.addMVar((nV_SG, nV_DG), name="PhiV", vtype=GRB.BINARY)
    m.update()
    if userConstrsGen:
        m.addConstrs(userConstrsGen(m=m, PhiE=PhiE, PhiV=PhiV))
    for i in range(nV_DG):
        m.addConstr(sum(PhiV[:, i]) == 1)
    for i in range(nE_DG):
        m.addConstr(sum(PhiE[:, i]) == 1)
    for eIdx_DG, (eI_DG, eJ_DG) in enumerate(E_DG):
        m.addConstr(S_SG @ PhiE[:, eIdx_DG] == PhiV[:, eI_DG])
        m.addConstr(D_SG @ PhiE[:, eIdx_DG] == PhiV[:, eJ_DG])
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
    solution_PhiE = solution[:(nE_SG * nE_DG)].reshape((nE_SG, nE_DG))
    solution_PhiV = solution[(nE_SG * nE_DG):].reshape((nV_SG, nV_DG))
    return (solution_PhiE, solution_PhiV)

if __name__ == "__main__":
    n_DG = 3
    n_SG = 4
    A_DG = np.array([1, 2, 2], dtype=np.int)
    A_SG = np.array([3, 1, 1, 2], dtype=np.int)
    W_DG = np.array([
        [0, 3, 1],
        [3, 0, 2],
        [1, 2, 0]
    ])
    W_SG = np.array([
        [0, 1, 2, 1],
        [1, 0, 1, 2],
        [2, 1, 0, 1],
        [1, 2, 1, 0]
    ])
    rho_SG = np.array([1, 1, 1, 1], dtype=np.int)
    (solution_PhiE, solution_PhiV) = abrr(n_DG, n_SG, np.reshape(A_DG, (1, -1)), np.reshape(A_SG, (1, -1)), W_DG, W_SG, rho_SG)
    print(solution_PhiE)
    print(solution_PhiV)
