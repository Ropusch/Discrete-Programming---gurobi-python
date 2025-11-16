import cvxpy as cp
import numpy as np

# --- Zmienne decyzyjne ---

x = cp.Variable((8, 8), boolean=True)
u = cp.Variable(8, nonneg=True, integer=True)

# --- Dane ---
W = 1000 * np.ones((8, 8))

W[0,1], W[1,0] = 2, 2
W[0,3], W[3,0] = 1, 1
W[0,2], W[2,0] = 4, 4
W[1,3], W[3,1] = 2, 2
W[2,3], W[3,2] = 4, 4

W[0,4], W[4,0] = 10, 10
W[2,5], W[5,2] = 2, 2
W[7,3], W[3,7] = 8, 8

W[4,5], W[5,4] = 4, 4
W[5,7], W[7,5] = 4, 4
W[4,6], W[6,4] = 2, 2
W[6,7], W[7,6] = 2, 2


# --- Ograniczenia ---
constraints = []

for i in range(8):
    constraints.append(cp.sum(x[i, :]) - x[i, i] == 1)
    constraints.append(cp.sum(x[:, i]) - x[i, i] == 1)

for i in range(1,8):
    constraints += [u[i] <= 8]
    constraints += [u[i] >= 2]

    for j in range(1,8):
        if i==j:
            continue
        constraints.append(u[i]-u[j]+8*x[i,j] <= 7)

# --- Funkcja celu ---
objective = cp.Minimize(cp.sum(cp.multiply(W, x))-cp.sum(W[i, i]*x[i, i]))


# --- Problem optymalizacyjny ---
problem = cp.Problem(objective, constraints)
problem.solve(solver=cp.GLPK_MI)  # solver dla MILP

# --- Wyniki ---
print("Status:", problem.status)
print("Wartość funkcji celu:", problem.value)
print("x =", x.value)