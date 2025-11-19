import gurobipy as gp
from gurobipy import GRB

# --- Model ---
model = gp.Model("zad4")

# --- Zmienne ---
a = model.addVar(vtype=GRB.INTEGER, name="a")
b = model.addVar(vtype=GRB.INTEGER, lb=1, ub=20, name="b")
d = model.addVar(lb=-GRB.INFINITY, name="d")  # free continuous

# --- Ograniczenia ---
model.addConstr(a - 3.14*b <= d)
model.addConstr(3.14*b - a <= d)

# --- Cel ---
model.setObjective(d, GRB.MINIMIZE)

# --- Solve ---
model.optimize()

# --- Wyniki ---
if model.status == GRB.OPTIMAL:
    print("OPTIMAL")
    for v in model.getVars():
        print(v.VarName, "=", v.X)
    print("Obj =", model.ObjVal)
    print("pi =", (a.X)/(b.X))
else:
    print("Status =", model.status)