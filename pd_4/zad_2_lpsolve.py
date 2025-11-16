import cvxpy as cp
import numpy as np

# --- Zmienne decyzyjne ---

v = cp.Variable(8, boolean=True)

x = cp.Variable(12, boolean=True)

# --- Dane ---
c = [0, 66, 35, 10, 34, 40, 43, 25]

w = [100, 25, 10, 40, 20, 40, 20, 60, 40, 10, 40, 20]


# --- Ograniczenia ---
constraints = []

constraints += [w @ x <= 200]

constraints += [
    x[0] + x[1] + x[2] + x[3] == 2 * v[0],
    x[1] + x[4] == 2 * v[1],
    x[3] + x[5] + x[6] == 2 * v[2],
    x[4] + x[2] + x[5] + x[7] == 2 * v[3],
    x[0] + x[8] + x[9] == 2 * v[4],
    x[6] + x[8] + x[10] == 2 * v[5],
    x[9] + x[11] == 2 * v[6],
    x[7] + x[10] + x[11] == 2 * v[7]
]

constraints += [
    x[1] + x[3] + x[4] + x[5] <= 3,
    x[8] + x[9] + x[10] + x[11] <= 3


]


# --- Funkcja celu ---
objective = cp.Maximize(c @ v)


# --- Problem optymalizacyjny ---
problem = cp.Problem(objective, constraints)
problem.solve(solver=cp.GLPK_MI)  # solver dla MILP

# --- Wyniki ---
print("Status:", problem.status)
print("Wartość funkcji celu:", problem.value)
print("x =", x.value)