import numpy as np
import gurobipy as gp
from gurobipy import GRB

def abgV(n_DG, n_SG, As_DG, As_SG, W_DG, W_SG, rho_SG, userConstrsGen=None):
    assert(len(As_DG) == len(As_SG))
    n_A = len(As_DG)
    m = gp.Model("abr")
    Phi = m.addMVar((n_DG, n_SG), name="Phi", vtype=GRB.BINARY)
    m.update()
    if userConstrsGen:
        m.addConstrs(userConstrsGen(m, Phi))
    for i in range(n_DG):
        m.addConstr(sum(Phi[i, :]) == 1)
    for k in range(n_A):
        for j in range(n_SG):
            m.addConstr(As_DG[k].T @ Phi[:, j] <= int(np.round(rho_SG[j] * As_SG[k][j])))
    loss = sum([
        sum([
            W_DG[i, j] * (Phi[j, :] @ W_SG @ Phi[i, :])
            for j in range(i)
        ])
        for i in range(n_DG)
    ])
    m.setObjective(loss, GRB.MINIMIZE)
    m.optimize()
    solution = m.getAttr("X")
    return np.reshape(solution, (n_DG, n_SG))

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
    print(abr(n_DG, n_SG, np.reshape(A_DG, (1, -1)), np.reshape(A_SG, (1, -1)), W_DG, W_SG, rho_SG))
