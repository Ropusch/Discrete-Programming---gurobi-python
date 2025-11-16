import cvxpy as cp
import numpy as np

# --- Zmienne decyzyjne ---

n = 6

x = cp.Variable((n, n), boolean=True)
u = cp.Variable(n, nonneg=True, integer=True)

# --- Dane ---
W = np.array([
    [100, 5, 9, 3, 2, 4],
    [4, 100, 6, 2, 2, 2],
    [3, 5, 100, 3, 3, 3],
    [2, 1, 4, 100, 4, 4],
    [2, 4, 3, 4, 100, 3],
    [3, 2, 3, 1, 2, 100]
])


# --- Ograniczenia ---
constraints = []

for i in range(n):
    constraints.append(cp.sum(x[i, :]) - x[i, i] == 1)
    constraints.append(cp.sum(x[:, i]) - x[i, i] == 1)

for i in range(1,n):
    constraints += [u[i] <= n]
    constraints += [u[i] >= 2]

    for j in range(1,n):
        if i==j:
            continue
        constraints.append(u[i]-u[j]+n*x[i,j] <= n-1)

# --- Funkcja celu ---
objective = cp.Minimize(cp.sum(cp.multiply(W, x))-cp.sum(W[i, i]*x[i, i]))


# --- Problem optymalizacyjny ---
problem = cp.Problem(objective, constraints)
problem.solve(solver=cp.GLPK_MI)  # solver dla MILP

# --- Wyniki ---
print("Status:", problem.status)
print("Wartość funkcji celu:", problem.value)
print("x =", x.value)
