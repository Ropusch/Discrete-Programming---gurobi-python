import cvxpy as cp
import numpy as np

# --- Zmienne decyzyjne ---

x = cp.Variable(4, integer=True, nonneg=True)

# --- Dane ---
w = [3, 7, 15, 25]

c = 102

# --- Ograniczenia ---
constraints = []

constraints += [w @ x == c]

# --- Funkcja celu ---
objective = cp.Minimize(cp.sum(x))

# --- Problem optymalizacyjny ---
problem = cp.Problem(objective, constraints)
problem.solve(solver=cp.GLPK_MI)  # solver dla MILP

# --- Wyniki ---
print("Status:", problem.status)
print("Wartość funkcji celu:", problem.value)
print("x =", x.value)