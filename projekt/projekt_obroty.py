import gurobipy as gp
from gurobipy import GRB
import numpy as np

# --- Dane --- czas: 0.40s; wynik= 2
# Wymiar = [6, 6]
# N = 3
# wymiary_k = [(1, 4), (2,3)]
# ile_k = [10, 3]
# k = len(ile_k)
# big_M = Wymiar[0]*Wymiar[1]/3

# --- Dane --- czas: 13.96s wynik = 3
Wymiar = [10, 13]
N = 5
wymiary_k = [(9, 5), (3, 5), (6, 4)]
ile_k = [2, 4, 8]
k = len(ile_k)
big_M = Wymiar[0]*Wymiar[1]/3

# # --- Dane --- czas: 8,71s; wynik= 7
# Wymiar = [8, 18]
# N = 8
# wymiary_k = [(7, 7), (2, 2), (4, 4), (6, 6)]
# ile_k = [3, 10, 8, 10]
# k = len(ile_k)
# big_M = Wymiar[0]*Wymiar[1]/3

# --- Dane --- czas: 0.88 s
# Wymiar = [10, 10]
# N = 5
# wymiary_k = [(2, 2), (3, 3), (4, 4)]
# ile_k = [6, 8, 5]
# k = len(ile_k)
# big_M = Wymiar[0]*Wymiar[1]/4


# --- Model ---
model = gp.Model("MILP_example")

# --- Zmienne decyzyjne ---
n = model.addVars(N, vtype=GRB.BINARY)
y = {}
for i in range(N):
    for j, (h, w) in enumerate(wymiary_k):
        if h == w:
            for a in range(Wymiar[0] - h + 1):
                for b in range(Wymiar[1] - w + 1):
                    y[i, (j+1), a, b] = model.addVar(
                        vtype=GRB.BINARY,
                        name=f"y_{i}_{(j+1)}_{a}_{b}"
                    )
        elif h != w:
            for a in range(Wymiar[0] - h + 1):
                for b in range(Wymiar[1] - w + 1):
                    y[i, (j+1), a, b] = model.addVar(
                        vtype=GRB.BINARY,
                        name=f"y_{i}_{(j+1)}_{a}_{b}")

            for a in range(Wymiar[0] - w + 1):
                for b in range(Wymiar[1] - h + 1):
                    y[i, -(j+1), a, b] = model.addVar(
                        vtype=GRB.BINARY,
                        name=f"y_{i}_{-(j+1)}_{a}_{b}")

# x = model.addVars(N, len(wymiary_k), Wymiar[0], Wymiar[1], vtype=GRB.BINARY)
x = {}
for i in range(N):
    for j, (h, w) in enumerate(wymiary_k):
        if h == w:
            for a in range(Wymiar[0]):
                for b in range(Wymiar[1]):
                    x[i, j+1, a, b] = model.addVar(
                        vtype=GRB.BINARY,
                        name=f"y_{i}_{j+1}_{a}_{b}"
                    )
        elif h != w:
            for a in range(Wymiar[0]):
                for b in range(Wymiar[1]):
                    x[i, j+1, a, b] = model.addVar(
                        vtype=GRB.BINARY,
                        name=f"y_{i}_{j+1}_{a}_{b}")

            for a in range(Wymiar[0]):
                for b in range(Wymiar[1]):
                    x[i, -(j+1), a, b] = model.addVar(
                        vtype=GRB.BINARY,
                        name=f"y_{i}_{-(j+1)}_{a}_{b}")

# --- Ograniczenia ---

for j, (h, w) in enumerate(wymiary_k):
    if h == w:
        model.addConstr(
            gp.quicksum(y[key] for key in y if key[1] == (j+1)) >= ile_k[j],
            name=f"limit_klockow_{(j+1)}")
    elif h != w:
        model.addConstr(
            gp.quicksum(y[key] for key in y if key[1] == (j+1) or key[1] == -(j+1)) >= ile_k[j],
            name=f"limit_klockow_{-(j+1)}")


for i in range(N):
    model.addConstr(
        gp.quicksum(y[key] for key in y if key[0] == i) <= big_M * n[i],
        name=f"limit_y_dla_n_{i}")


for i in range(N):
    for a in range(Wymiar[0]):
        for b in range(Wymiar[1]):
            model.addConstr(
                gp.quicksum(x[i, w, a, b] for w in sorted({key[1] for key in x})) <= 1,
                name=f"exactly_one_type_i{i}_b{a}_c{b}")


for i in range(N):
    for j in range(k):
        h, w = wymiary_k[j]
        if h == w:
            pos = [(a, b) for a in range(Wymiar[0] - h + 1) for b in range(Wymiar[1] - w + 1)]
            for idx1, (a, b) in enumerate(pos):
                model.addConstr(
                    gp.quicksum(x[i, (j+1), a+s, b+t] for s in range(h) for t in range(w)) >= h*w * y[i, (j+1), a, b],
                    name=f"no_overlap_y_same_obj_j{(j+1)}_i{i}_a{a}_b{b}")
        elif h != w:
            pos = [(a, b) for a in range(Wymiar[0] - h + 1) for b in range(Wymiar[1] - w + 1)]
            for idx1, (a, b) in enumerate(pos):
                model.addConstr(
                    gp.quicksum(x[i, (j + 1), a + s, b + t] for s in range(h) for t in range(w)) >= h * w * y[i, (j + 1), a, b],
                    name=f"no_overlap_y_same_obj_j{(j + 1)}_i{i}_a{a}_b{b}")

            pos = [(a, b) for a in range(Wymiar[0] - w + 1) for b in range(Wymiar[1] - h + 1)]
            for idx1, (a, b) in enumerate(pos):
                model.addConstr(
                    gp.quicksum(x[i, -(j + 1), a + s, b + t] for s in range(w) for t in range(h)) >= h * w * y[i, -(j + 1), a, b],
                    name=f"no_overlap_y_same_obj_j{-(j + 1)}_i{i}_a{a}_b{b}")



for i in range(N):
    for j in range(k):
        h, w = wymiary_k[j]
        if h == w:
            pos = [(a, b) for a in range(Wymiar[0] - h + 1) for b in range(Wymiar[1] - w + 1)]
            for idx1, (a, b) in enumerate(pos):
                model.addConstr(
                    gp.quicksum(y[i, (j+1), a+s, b+t] for s in range(h) for t in range(w) if (i, (j+1), a+s, b+t) in y) <= 1,
                    name=f"no_overlap_y_same_obj_j{(j+1)}_i{i}_a{a}_b{b}")
        elif h != w:
            pos = [(a, b) for a in range(Wymiar[0] - h + 1) for b in range(Wymiar[1] - w + 1)]
            for idx1, (a, b) in enumerate(pos):
                model.addConstr(
                    gp.quicksum(y[i, (j + 1), a + s, b + t] for s in range(h) for t in range(w) if (i, (j + 1), a + s, b + t) in y) <= 1,
                    name=f"no_overlap_y_same_obj_j{(j + 1)}_i{i}_a{a}_b{b}")

            pos = [(a, b) for a in range(Wymiar[0] - w + 1) for b in range(Wymiar[1] - h + 1)]
            for idx1, (a, b) in enumerate(pos):
                model.addConstr(
                    gp.quicksum(y[i, -(j + 1), a + s, b + t] for s in range(w) for t in range(h) if (i, -(j + 1), a + s, b + t) in y) <= 1,
                    name=f"no_overlap_y_same_obj_j{(j + 1)}_i{i}_a{a}_b{b}")


# --- Funkcja celu ---
objective = (gp.quicksum(n[i] for i in range(N)))

model.setObjective(objective, GRB.MINIMIZE)

# --- Rozwiązanie ---
model.optimize()

# --- Wyniki ---
def print_colored_matrix(m):
    color_map = {
        -1: 93,  # yellow
        -2: 94,  # blue
        -3: 92,  # green
        -4: 91,  # red
        -5: 95,  # magenta
        -6: 96,  # cyan
        -7: 90,  # grey
        -8: 94,  # bright blue
        -9: 91,  # bright red
        -10: 92,  # bright green
        0: 97,   # white
        1: 93,   # yellow
        2: 94,   # blue
        3: 92,   # green
        4: 91,   # red
        5: 95,   # magenta
        6: 96,   # cyan
        7: 90,   # grey
        8: 94,   # bright blue
        9: 91,   # bright red
        10: 92,  # bright green
    }

    for row in m:
        line = ""
        for val in row:
            fg = color_map.get(val, 97)  # domyślnie biały
            line += f"\033[{fg}m{val:2d}\033[0m "
        print(line)


if model.status == GRB.OPTIMAL:
    print(f"Status: OPTIMAL")
    print(f"Wartość funkcji celu: {model.objVal}")

    for i in range(N):
        if n[i].X < 0.5:
            continue
        mat = np.zeros((Wymiar[0], Wymiar[1]), dtype=int)
        mat_y = np.zeros((Wymiar[0], Wymiar[1]), dtype=int)
        for (ii, j, a, b), var in y.items():
            if ii != i:
                continue
            if var.X > 0.5:
                if j > 0:
                    h, w = wymiary_k[j-1]
                    for da in range(h):
                        for db in range(w):
                            mat[a + da, b + db] = j
                elif j < 0:
                    w, h = wymiary_k[abs(j+1)]
                    for da in range(h):
                        for db in range(w):
                            mat[a + da, b + db] = j

        print(f"Plan wycinanai na płytce nr {i}:")
        print_colored_matrix(mat)
        print("\n")

else:
    print(f"Status: {model.status}")











########################################################

# def stopping_callback(model, where):
#     if where == GRB.Callback.MIP:
#         runtime = model.cbGet(GRB.Callback.RUNTIME)
#         best = model.cbGet(GRB.Callback.MIP_OBJBST)
#         bound = model.cbGet(GRB.Callback.MIP_OBJBND)
#
#         # brak rozwiązania jeszcze
#         if best == GRB.INFINITY or best == 0:
#             return
#
#         gap = abs(best - bound) / abs(best)
#
#
#         if gap < 0.15 and runtime > 60:
#             print(f"\nSTOP: gap={gap:.2%}, time={runtime:.1f}s")
#             model.terminate()
#
#         elif gap < 0.50 and runtime > 500:
#             print(f"\nSTOP: gap={gap:.2%}, time={runtime:.1f}s")
#             model.terminate()
#
#
# # model.optimize(stopping_callback)
