import gurobipy as gp
from gurobipy import GRB

# --- Dane ---
c = [2, 3, 5]

# --- Model ---
model = gp.Model("MILP_example")

# --- Zmienne decyzyjne ---
x = model.addVars(3, 3, vtype=GRB.INTEGER, lb=0, name="x")

# --- Ograniczenia ---


model.addConstr(
    gp.quicksum(x[0, j] * c[j] for j in range(3)) +
    3 * gp.quicksum(x[1, j] * c[j] for j in range(3)) +
    gp.quicksum(x[2, j] * c[j] for j in range(3))
    <= 20,
)

model.addConstr(
    2 * gp.quicksum(x[0, j] * c[j] for j in range(3)) -
    gp.quicksum(x[1, j] * c[j] for j in range(3)) +
    5 * gp.quicksum(x[2, j] * c[j] for j in range(3))
    <= 20,
)

for i in range(3):
    model.addConstr(gp.quicksum(x[i, j] for j in range(3)) == 1)

# --- Funkcja celu ---
# Maximize (x[0, :] @ c) + 5*(x[1, :] @ c) + 3*(x[2, :] @ c)
objective = (
    gp.quicksum(x[0, j] * c[j] for j in range(3)) +
    5 * gp.quicksum(x[1, j] * c[j] for j in range(3)) +
    3 * gp.quicksum(x[2, j] * c[j] for j in range(3))
)
model.setObjective(objective, GRB.MAXIMIZE)

# --- Rozwiązanie ---
model.optimize()

# --- Wyniki ---
if model.status == GRB.OPTIMAL:
    print(f"Status: OPTIMAL")
    print(f"Wartość funkcji celu: {model.objVal}")
    print("x =")
    for i in range(3):
        print([x[i, j].X for j in range(3)])
else:
    print(f"Status: {model.status}")
