import gurobipy as gp
from gurobipy import GRB
import  numpy as np

# --- Dane ---
c = [
    [7, 3, 6, 2, 1],
    [8, 4, 9, 1, 2],
    [2, 6, 6, 2, 1],
    [3, 5, 2, 1, 8],
    [8, 2, 5, 10, 8],
    [2, 2, 3, 4, 1]
]
f = [1000, 1200, 2000, 1500, 1600]
b = [110, 90, 350, 80, 120, 150]

# --- Model ---
model = gp.Model("MILP_example")

# --- Zmienne decyzyjne ---
x = model.addVars(5, vtype=GRB.BINARY, name="x")
y = model.addVars(6, 5, vtype=GRB.INTEGER, lb=0, name="y")


# --- Ograniczenia ---
for j in range(5):
    model.addConstr(
        gp.quicksum(y[i, j] for i in range(6)) <= 300*x[j]
    )
for i in range(6):
    model.addConstr(
        gp.quicksum(y[i, j] for j in range(5)) >= b[i]
    )

# --- Funkcja celu ---
objective = (
        gp.quicksum(f[j] * x[j] for j in range(5)) +
        gp.quicksum(c[i][j] * y[i, j] for i in range(6) for j in range(5))
)

model.setObjective(objective, GRB.MINIMIZE)

# --- Rozwiązanie ---
model.optimize()

# --- Wyniki ---
x_values = [x[j].x for j in x.keys()]
Y_matrix = np.array([[y[i, j].x for j in range(5)] for i in range(6)])

if model.status == GRB.OPTIMAL:
    print(f"Status: OPTIMAL")
    print(f"Wartość funkcji celu: {model.objVal}")
    print("x =", x_values)
    print("y =\n", Y_matrix)
else:
    print(f"Status: {model.status}")
