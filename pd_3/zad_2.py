import cvxpy as cp

# --- Zmienne decyzyjne ---
x = cp.Variable(10, integer=True)
y = cp.Variable(10, integer=True)

# --- Dane ---
profit_x = [10, 27, 19, 15, 10, 12, 7, 12, 13, 14]
profit_y = [10, 27, 19, 15, 10, 12, 7, 12, 13, 14]

cost_x = [5, 7, 9, 11, 6, 8, 5, 5, 6, 8]
cost_y = [8, 5, 6, 7, 11, 5, 12, 8, 10, 4]

rhs = [3, 2, 3, 2, 2, 4, 2, 3, 2, 1]  # ograniczenia x_i + y_i <= rhs_i

# --- Ograniczenia ---
constraints = []

# Zasoby
constraints += [
    cost_x @ x <= 30,
    cost_y @ y <= 50
]

# Ograniczenia sum
for i in range(10):
    constraints.append(x[i] + y[i] <= rhs[i])

# Nieujemność
constraints += [x >= 0, y >= 0]

# --- Funkcja celu ---
objective = cp.Maximize(profit_x @ x + profit_y @ y)

# --- Problem optymalizacyjny ---
problem = cp.Problem(objective, constraints)
problem.solve(solver=cp.GLPK_MI)  # wbudowany solver MILP

# --- Wyniki ---
print("Status:", problem.status)
print("Wartość funkcji celu:", problem.value)
print("x =", x.value)
print("y =", y.value)