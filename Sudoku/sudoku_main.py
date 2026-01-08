import gurobipy as gp
from gurobipy import GRB
import numpy as np

# --- Dane ---
sudoku = [
    [5, 0, 0, 0, 0, 2, 0, 0, 0],
    [0, 4, 2, 0, 0, 0, 8, 0, 7],
    [0, 9, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 4, 3, 0],
    [8, 0, 0, 9, 0, 4, 2, 0, 0],
    [4, 7, 3, 6, 0, 0, 0, 8, 1],
    [0, 8, 0, 0, 0, 0, 7, 0, 9],
    [0, 3, 0, 0, 0, 9, 0, 1, 2],
    [2, 1, 9, 0, 7, 0, 0, 0, 0],
]



# --- Model ---
model = gp.Model("MILP_example")

# --- Zmienne decyzyjne ---
x = model.addVars(9, 9, 9, vtype=GRB.BINARY)
z = model.addVars(1, vtype=GRB.BINARY)


# --- Ograniczenia ---
for i in range(9):
    for j in range(9):
        model.addConstr(
            gp.quicksum(x[i, j, k] for k in range(9)) == 1
        )

for k in range(9):
    for j in range(9):
        model.addConstr(
            gp.quicksum(x[i, j, k] for i in range(9)) == 1
        )
        model.addConstr(
            gp.quicksum(x[j, i, k] for i in range(9)) == 1
        )


for k in range(9):
    for t in range(3):
        for s in range(3):
            model.addConstr(
                gp.quicksum(x[3*t+i, 3*s+j, k] for i in range(3) for j in range(3)) == 1
            )

for i in range(9):
    for j in range(9):
        if sudoku[i][j] !=0:
            model.addConstr(
                x[i, j, sudoku[i][j]-1] == 1
            )

# --- Funkcja celu ---
objective = (z[0])

model.setObjective(objective, GRB.MINIMIZE)

# --- Rozwiązanie ---
model.optimize()

# --- Wyniki ---
x_mat = np.zeros((9, 9), dtype=int)

for i in range(9):
    for j in range(9):
        for k in range(9):
            if x[i, j, k].X > 0.5:
                x_mat[i, j] = k + 1
                break

if model.status == GRB.OPTIMAL:
    print(f"Status: OPTIMAL")
    print(f"Wartość funkcji celu: {model.objVal}")
    print("x =\n", x_mat)
else:
    print(f"Status: {model.status}")
