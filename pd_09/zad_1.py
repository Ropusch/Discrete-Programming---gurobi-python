import gurobipy as gp
from gurobipy import GRB
import  numpy as np

# --- Dane ---
c = [
    [2, 3, 1, 0, 0],
    [4, 5, 0, 0, 0],
    [2, 4, 1, 5, 0]
]


# --- Model ---
model = gp.Model("MILP_example")

# --- Zmienne decyzyjne ---
p = model.addVars(1, vtype=GRB.INTEGER)
x = model.addVars(3, 5, vtype=GRB.BINARY)


# --- Ograniczenia ---
for i in range(3):
    model.addConstr(
        gp.quicksum(x[i, j] for j in range(5)) == 1
    )

for i in range(3):
    for j in range(5-np.count_nonzero(c[i])+1, 5):
        model.addConstr(
            x[i, j] <= 0
        )

for t in range(5):
    expr = gp.quicksum(
        x[i, t-k] * c[i][k]
        for i in range(3)
        for k in range(t+1)
    )
    model.addConstr(expr <= p[0])



# --- Funkcja celu ---
objective = (p[0])


model.setObjective(objective, GRB.MINIMIZE)

# --- Rozwiązanie ---
model.optimize()

# --- Wyniki ---
x_mat = np.array([[x[i, j].x for j in range(5)] for i in range(3)])

if model.status == GRB.OPTIMAL:
    print(f"Status: OPTIMAL")
    print(f"Wartość funkcji celu: {model.objVal}")
    print("x =\n", x_mat)
else:
    print(f"Status: {model.status}")
