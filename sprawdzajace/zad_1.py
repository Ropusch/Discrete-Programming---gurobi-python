import gurobipy as gp
from gurobipy import GRB
import  numpy as np

# --- Dane ---
A = [
    [0.05, 0.06, None, 0.12, 0.06],   # A
    [0.02, 0.05, 0.07, 0.05, 0.10],   # B
    [None, None, 0.10, 0.11, 0.08],   # C
    [0.01, None, 0.03, 0.04, 0.01]    # D
]
koszty_produkcji_proszk = [1.56, 2.2, 2.0, 1.4]
koszty_utrzymania_linii = [50, 30, 35, 75, 90]
wymagania = [1000, 1200, 1000, 1100]
limit_h = 60

# --- Model ---
model = gp.Model("MILP_example")

# --- Zmienne decyzyjne ---
x = model.addVars(5, vtype=GRB.BINARY)
y = {}
for i in range(4):
    for j in range(5):
        if A[i][j] is not None:
            y[i, j] = model.addVar(lb=0, vtype=GRB.INTEGER)


# --- Ograniczenia ---
for j in range(5):
    model.addConstr(
        gp.quicksum(A[i][j] * y[i, j] for (i, j2) in y if j2 == j) <= 60 * x[j]
    )

for i in range(4):
    model.addConstr(
        gp.quicksum(y[i, j] for (i2, j) in y if i2 == i) >= wymagania[i]
    )

# --- Funkcja celu ---
objective = (
        gp.quicksum(koszty_utrzymania_linii[j] * x[j] for j in range(5)) +
        gp.quicksum(koszty_produkcji_proszk[i] * y[i, j] for (i, j2) in y if j2 == j)
)

model.setObjective(objective, GRB.MINIMIZE)

# --- Rozwiązanie ---
model.optimize()

# --- Wyniki ---
x_values = [x[j].x for j in x.keys()]
Y_matrix = np.zeros((4, 5))
for i in range(4):
    for j in range(5):
        if (i, j) in y:
            Y_matrix[i, j] = y[i, j].x
        else:
            Y_matrix[i, j] = 0

if model.status == GRB.OPTIMAL:
    print(f"Status: OPTIMAL")
    print(f"Wartość funkcji celu: {model.objVal}")
    print("x =", x_values)
    print("y =\n", Y_matrix)
else:
    print(f"Status: {model.status}")
