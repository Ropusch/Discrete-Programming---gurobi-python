import gurobipy as gp
from gurobipy import GRB

# --- Model ---
model = gp.Model("zad2")

# --- Zmienne główne (bin) ---
a = model.addVars(4, vtype=GRB.BINARY, name="a")  # a1..a4
t = model.addVars(4, vtype=GRB.BINARY, name="t")  # t1..t4
r = model.addVars(4, vtype=GRB.BINARY, name="r")  # r1..r4
k = model.addVars(4, vtype=GRB.BINARY, name="k")  # k1..k4

# --- Zmienne pomocnicze (mnożenie binarne) ---
# a*t
at = model.addVars(4, 4, vtype=GRB.BINARY, name="at")  # at[i,j] = a[i]*t[j]
# a*r
ar = model.addVars(4, 4, vtype=GRB.BINARY, name="ar")
# a*k
ak = model.addVars(4, 4, vtype=GRB.BINARY, name="ak")

# --- Ograniczenia sumy do 1 ---
model.addConstr(sum(a[i] for i in range(4)) == 1)
model.addConstr(sum(t[j] for j in range(4)) == 1)
model.addConstr(sum(r[j] for j in range(4)) == 1)
model.addConstr(sum(k[j] for j in range(4)) == 1)

# --- Ograniczenia sumy po wierszach (a[i]+t[i]+r[i]+k[i]==1) ---
for i in range(4):
    model.addConstr(a[i] + t[i] + r[i] + k[i] == 1)

# --- Ograniczenia liniowe dla mnożenia binarnego ---
for i in range(4):
    for j in range(4):
        model.addConstr(2*at[i,j] <= a[i] + t[j])
        model.addConstr(at[i,j] >= a[i] + t[j] - 1)

        model.addConstr(2*ar[i,j] <= a[i] + r[j])
        model.addConstr(ar[i,j] >= a[i] + r[j] - 1)

        model.addConstr(2*ak[i,j] <= a[i] + k[j])
        model.addConstr(ak[i,j] >= a[i] + k[j] - 1)

# --- Funkcja celu (przykładowe wagi z Twojego opisu) ---
obj = (
    3*at[0,1] + 6*at[0,2] + 9*at[0,3] +
    3*at[1,0] + 3*at[1,2] + 6*at[1,3] +
    6*at[2,0] + 3*at[2,1] + 3*at[2,3] +
    9*at[3,0] + 6*at[3,1] + 3*at[3,2] +
    2*ar[0,1] + 4*ar[0,2] + 6*ar[0,3] +
    2*ar[1,0] + 2*ar[1,2] + 4*ar[1,3] +
    4*ar[2,0] + 2*ar[2,1] + 2*ar[2,3] +
    6*ar[3,0] + 4*ar[3,1] + 2*ar[3,2] +
    1*ak[0,1] + 2*ak[0,2] + 3*ak[0,3] +
    1*ak[1,0] + 1*ak[1,2] + 2*ak[1,3] +
    2*ak[2,0] + 1*ak[2,1] + 1*ak[2,3] +
    3*ak[3,0] + 2*ak[3,1] + 1*ak[3,2]
)

model.setObjective(obj, GRB.MINIMIZE)

# --- Optymalizacja ---
model.optimize()

# --- Wyniki ---
if model.status == GRB.OPTIMAL:
    print("OPTIMAL")
    for v in model.getVars():
        print(v.VarName, "=", v.X)
    print("Obj =", model.ObjVal)
else:
    print("Status =", model.status)
