import cvxpy as cp

# --- Zmienne decyzyjne ---

x = cp.Variable(10, boolean=True)

xb = cp.Variable(10, integer=True, nonneg=True)
yb = cp.Variable(10, integer=True, nonneg=True)

# --- Dane ---
coeffs = [10, 27, 19, 15, 10, 12, 7, 12, 13, 14]
masa = [5, 7, 9, 11, 6, 8, 5, 5, 6, 8]

# --- Ograniczenia ---
constraints = []

constraints += [
    masa @ x <= 30
]

constraints_b = []

constraints_b += [
    masa @ xb <= 30,
    masa @ yb <= 30
]

for i in range(10):
    constraints_b += [ xb[i]+yb[i] <= 2 ]

# --- Funkcja celu ---
objective = cp.Maximize(coeffs @ x)

objective_b = cp.Maximize(coeffs @ xb + coeffs @ yb)

# --- Problem optymalizacyjny ---
problem = cp.Problem(objective, constraints)
problem.solve(solver=cp.GLPK_MI)  # solver dla MILP

problem_b = cp.Problem(objective_b, constraints_b)
problem_b.solve(solver=cp.GLPK_MI)  # solver dla MILP

# --- Wyniki ---
print("Status:", problem.status)
print("Wartość funkcji celu:", problem.value)
print("x =", x.value)

print("\n 1b)")
print("Status:", problem_b.status)
print("Wartość funkcji celu:", problem_b.value)
print(xb.value, yb.value)