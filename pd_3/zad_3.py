import cvxpy as cp

# --- Zmienne decyzyjne ---

# macierze 6×10 dla x,y,z,s,t,u
x = cp.Variable(10, integer=True)
y = cp.Variable(10, integer=True)
z = cp.Variable(10, integer=True)
s = cp.Variable(10, integer=True)
t = cp.Variable(10, integer=True)
u = cp.Variable(10, integer=True)

# binarne zmienne p
p = cp.Variable(6, boolean=True)  # [px, py, pz, ps, pt, pu]

# --- Dane ---
coeffs = [5, 7, 9, 11, 6, 8, 5, 5, 6, 8]
rhs = [3, 2, 3, 2, 2, 4, 2, 3, 2, 1]  # suma w kolumnach

# --- Ograniczenia ---
constraints = []

# ograniczenia typu "zasobowego"
constraints += [
    coeffs @ x <= 50 * p[0],
    coeffs @ y <= 50 * p[1],
    coeffs @ z <= 50 * p[2],
    coeffs @ s <= 50 * p[3],
    coeffs @ t <= 50 * p[4],
    coeffs @ u <= 50 * p[5]
]

# ograniczenia sum w kolumnach
for j in range(10):
    constraints.append(x[j] + y[j] + z[j] + s[j] + t[j] + u[j] == rhs[j])

# dolne granice na zmienne całkowite
constraints += [
    x >= 0, y >= 0, z >= 0, s >= 0, t >= 0, u >= 0
]

# --- Funkcja celu ---
objective = cp.Minimize(cp.sum(p))

# --- Problem optymalizacyjny ---
problem = cp.Problem(objective, constraints)
problem.solve(solver=cp.GLPK_MI)  # solver dla MILP

# --- Wyniki ---
print("Status:", problem.status)
print("Wartość funkcji celu:", problem.value)
print("p =", p.value)