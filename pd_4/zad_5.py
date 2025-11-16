import cvxpy as cp
import numpy as np

# --- Zmienne decyzyjne ---

x = cp.Variable((3,3), integer=True, nonneg=True)

# --- Dane ---
c = [2, 3, 5]


# --- Ograniczenia ---
constraints = []

constraints += [
    (x[0, :] @ c) + 3*(x[1, :] @ c) + (x[2, :] @ c) <= 20,
    2*(x[0, :] @ c) + (-1)*(x[1, :] @ c) + 5*(x[2, :] @ c) <= 20
]

constraints += [
    cp.sum(x[0, :]) == 1,
    cp.sum(x[1, :]) == 1,
    cp.sum(x[2, :]) == 1
]

# --- Funkcja celu ---
objective = cp.Maximize((x[0, :] @ c) + 5*(x[1, :] @ c) + 3*(x[2, :] @ c))

# --- Problem optymalizacyjny ---
problem = cp.Problem(objective, constraints)
problem.solve(solver=cp.GUROBI)  # solver dla MILP

# --- Wyniki ---
print("Status:", problem.status)
print("Wartość funkcji celu:", problem.value)
print("x =", x.value)