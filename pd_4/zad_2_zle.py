import cvxpy as cp
import numpy as np

# --- Zmienne decyzyjne ---

x = cp.Variable((8, 8), boolean=True)
u = cp.Variable(8, nonneg=True, integer=True)
v = cp.Variable(8, boolean=True)

c = [0, 66, 35, 10, 34, 40, 43, 25]

# --- Dane ---
W = 1000 * np.ones((8, 8))

W[0,1], W[1,0] = 25, 25
W[0,3], W[3,0] = 10, 10
W[0,2], W[2,0] = 40, 40
W[1,3], W[3,1] = 20, 20
W[2,3], W[3,2] = 40, 40

W[0,4], W[4,0] = 10, 10
W[2,5], W[5,2] = 20, 20
W[7,3], W[3,7] = 60, 60

W[4,5], W[5,4] = 40, 40
W[5,7], W[7,5] = 40, 40
W[4,6], W[6,4] = 10, 10
W[6,7], W[7,6] = 20, 20


# --- Ograniczenia ---
constraints = []

constraints += [cp.sum(cp.multiply(W, x)) <= 200]

for i in range(8):
    constraints.append(cp.sum(x[i, :]) - x[i, i] == 1*v[i])
    constraints.append(cp.sum(x[:, i]) - x[i, i] == 1*v[i])

# for i in range(1,8):
#     constraints += [u[i] <= 8]
#     constraints += [u[i] >= 2]
#
#     for j in range(1,8):
#         if i==j:
#             continue
#         constraints.append(u[i]-u[j]+8*x[i,j] <= 7)

# --- Funkcja celu ---
objective = cp.Maximize(c @ v)


# --- Problem optymalizacyjny ---
problem = cp.Problem(objective, constraints)
problem.solve(solver=cp.GLPK_MI)  # solver dla MILP

# --- Wyniki ---
print("Status:", problem.status)
print("Wartość funkcji celu:", problem.value)
print("x =", x.value)