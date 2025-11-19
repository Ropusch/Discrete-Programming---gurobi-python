import gurobipy as gp
from gurobipy import GRB

# --- Model ---
model = gp.Model("zad3")

# --- Zmienne ---
x1 = model.addVar(vtype=GRB.BINARY, name="x1")
x2 = model.addVar(vtype=GRB.BINARY, name="x2")
x3 = model.addVar(vtype=GRB.INTEGER, name="x3")
x4 = model.addVar(vtype=GRB.INTEGER, name="x4")
m   = model.addVar(vtype=GRB.INTEGER, lb=-GRB.INFINITY, name="m")   # free int

# --- Ograniczenia ---
model.addConstr(x1 + 3*x2 - x3 - x4 <= m)
model.addConstr(x1 + x2 - x3 + x4 <= m)
model.addConstr(x1 - 2*x2 + x3 - 3*x4 <= m)

model.addConstr(x3 <= 2)
model.addConstr(x4 <= 2)

# --- Cel ---
model.setObjective(m, GRB.MINIMIZE)

# --- Solve ---
model.optimize()

# --- Wyniki ---
if model.status == GRB.OPTIMAL:
    print("OPTIMAL")
    for v in model.getVars():
        print(v.VarName, "=", v.X)
    print("Obj =", model.ObjVal)
else:
    print("Status =", model.status)