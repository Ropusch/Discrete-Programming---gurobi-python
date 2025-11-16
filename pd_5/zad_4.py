import gurobipy as gp
from gurobipy import GRB
import  numpy as np

# --- Dane ---
z = [3, 8, 4, 6, 3, 8, 11, 7, 7, 6, 3, 9]
kj = [5, 4, 3, 7,  4, 3, 4, 6, 3, 5, 4, 5]
m = [2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1]
kl = np.ones(12)
kp = [10, 16, 20, 43, 19, 45, 30, 22, 25, 12, 13, 33]
M = gp.quicksum(z[i] for i in range(12)) + 1
# --- Model ---
model = gp.Model("MILP_example")

# --- Zmienne decyzyjne ---
x = model.addVars(12, vtype=GRB.INTEGER, lb=0, name="x")
p = model.addVars(12, vtype=GRB.BINARY, name="p")
s = model.addVars(13, vtype=GRB.INTEGER, lb=0, name="s")
l = model.addVars(13, vtype=GRB.INTEGER, lb=0, name="l")


# --- Ograniczenia ---
model.addConstr(s[0] == 0)
model.addConstr(l[0] == 0)
model.addConstr(l[12] == 0)

for t in range(12):
    model.addConstr(x[t] <= M * p[t])

for t in range(12):
    model.addConstr(
        s[t+1] == s[t] + x[t] - z[t] + l[t+1] - l[t]
    )

# --- Funkcja celu ---
objective = (
        gp.quicksum(kp[t]*p[t] for t in range(12)) + gp.quicksum(kj[t] * x[t] for t in range(12)) +
        gp.quicksum(m[t] * s[t+1] for t in range(12)) + gp.quicksum(kl[t] * l[t+1] for t in range(12))
)

model.setObjective(objective, GRB.MINIMIZE)

# --- Rozwiązanie ---
model.optimize()

# --- Wyniki ---
x_values = [x[j].x for j in x.keys()]
p_values = [p[j].x for j in p.keys()]

if model.status == GRB.OPTIMAL:
    print(f"Status: OPTIMAL")
    print(f"Wartość funkcji celu: {model.objVal}")
    print("x =", x_values)
    print("p =", p_values)
else:
    print(f"Status: {model.status}")

