import gurobipy as gp
from gurobipy import GRB
import numpy as np

# --- Dane ---

A = [
    [12, 9,  15, 8],
    [7,  20, 10, 12],
    [9,  9,  15, 11],
    [5,  15, 15, 16]
]

# --- Model ---
model = gp.Model("MILP_example")

# --- Zmienne decyzyjne ---
X = model.addVars(4, 4, vtype=GRB.BINARY)

# --- Ograniczenia ---
for i in range(4):
    model.addConstr(gp.quicksum(X[i, j] for j in range(4)) == 1)

for j in range(4):
    model.addConstr(gp.quicksum(X[i, j] for i in range(4)) == 1)

# --- Funkcja celu ---
objective = (
    gp.quicksum(A[i][j] * X[i, j] for i in range(4) for j in range(4))
)

model.setObjective(objective, GRB.MINIMIZE)

# --- Rozwiązanie ---
model.optimize()

# --- Wyniki ---

x_values = np.array([[X[i, j].x for j in range(4)] for i in range(4)])
if model.status == GRB.OPTIMAL:
    print(f"Status: OPTIMAL")
    print(f"Wartość funkcji celu: {model.objVal}")
    print("X =\n", x_values)
else:
    print(f"Status: {model.status}")