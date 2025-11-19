import gurobipy as gp
from gurobipy import GRB
import  numpy as np

# --- Dane ---

# --- Model ---
model = gp.Model("MILP_example")

# --- Zmienne decyzyjne ---
x = model.addVars(5, vtype=GRB.BINARY)
y = model.addVars(7, vtype=GRB.BINARY)

# --- Ograniczenia ---
model.addConstrs(c for c in [

    3*y[0] <= x[0] + x[2] + x[4],
    y[0] >= x[0] + x[2] + x[4] - 2,

    2*y[1] <= x[0] + x[1],
    y[1] >= x[0] + x[1] - 1,

    2*y[2] <= x[0] + x[2],
    y[2] >= x[0] + x[2] - 1,

    2*y[3] <= x[0] + x[3],
    y[3] >= x[0] + x[3] - 1,

    2*y[4] <= x[1] + x[2],
    y[4] >= x[1] + x[2] - 1,

    2*y[5] <= x[1] + x[3],
    y[5] >= x[1] + x[3] - 1,

    2*y[6] <= x[2] + x[3],
    y[6] >= x[2] + x[3] - 1
])

# --- Funkcja celu ---
objective = (
    y[0] + 5*y[1] + 6*y[2] + 5*y[3] + 4*y[4] + 3*y[5] + 8*y[6] - 4*x[0] - 8*x[1] - 7*x[2] - 5*x[3] - 6*x[4]
)

model.setObjective(objective, GRB.MAXIMIZE)

# --- Rozwiązanie ---
model.optimize()

# --- Wyniki ---
x_values = [x[j].x for j in x.keys()]
y_values = [y[j].x for j in y.keys()]

if model.status == GRB.OPTIMAL:
    print(f"Status: OPTIMAL")
    print(f"Wartość funkcji celu: {model.objVal}")
    print("x =", x_values)
    print("y =", y_values)
else:
    print(f"Status: {model.status}")
