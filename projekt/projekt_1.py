import gurobipy as gp
from gurobipy import GRB
import numpy as np

# --- Dane --- czas: 365s wynik = 7
# Wymiar = [15, 12]
# N = 8
# wymiary_k = [(10, 10), (3, 3), (4, 4), (6, 6)]
# ile_k = [3, 20, 14, 10]
# k = len(ile_k)
# big_M = Wymiar[0]*Wymiar[1]/3

# --- Dane --- czas: 8,71s; wynik= 7
Wymiar = [8, 18]
N = 8
wymiary_k = [(7, 7), (2, 2), (4, 4), (6, 6)]
ile_k = [3, 10, 8, 10]
k = len(ile_k)
big_M = Wymiar[0]*Wymiar[1]/3

# --- Dane --- czas: 0.88 s
# Wymiar = [10, 10]
# N = 5
# wymiary_k = [(2, 2), (3, 3), (4, 4)]
# ile_k = [6, 8, 5]
# k = len(ile_k)
# big_M = Wymiar[0]*Wymiar[1]/4

# --- zad 3 z ćwiczeń --- niestety zbyt długo trwa
# Wymiar = [50, 50]
# N = 3
# wymiary_k = [(3, 3), (4, 4), (5, 5), (7, 7), (8, 8), (10, 10), (12, 12), (15, 15), (16, 16), (17, 17)]
# ile_k = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
# k = len(ile_k)
# big_M = Wymiar[0]*Wymiar[1]/9

# Wymiar = [30, 30] #inny zestaw do testowania - 30x30
# N = 5
# wymiary_k = [(10, 10), (12, 12), (15, 15), (16, 16)]
# ile_k = [2, 2, 2, 3]
# k = len(ile_k)
# big_M = Wymiar[0]*Wymiar[1]/100

# --- Model ---
model = gp.Model("MILP_example")

# --- Zmienne decyzyjne ---
n = model.addVars(N, vtype=GRB.BINARY)
y = {}
for i in range(N):  # obiekty
    for j, (h, w) in enumerate(wymiary_k):
        for a in range(Wymiar[0] - h + 1):
            for b in range(Wymiar[1] - w + 1):
                y[i, j, a, b] = model.addVar(
                    vtype=GRB.BINARY,
                    name=f"y_{i}_{j}_{a}_{b}"
                )
x = model.addVars(N, len(wymiary_k), Wymiar[0], Wymiar[1], vtype=GRB.BINARY)

# --- Ograniczenia ---

for j in range(k):
    model.addConstr(
        gp.quicksum(y[key] for key in y if key[1] == j) >= ile_k[j],
        name=f"limit_klockow_{j}"
    )


for i in range(N):
    model.addConstr(
        gp.quicksum(
            y[key]
            for key in y
            if key[0] == i
        ) <= big_M * n[i],
        name=f"limit_y_dla_n_{i}"
    )


for i in range(N):
    for a in range(Wymiar[0]):
        for b in range(Wymiar[1]):
            model.addConstr(
                gp.quicksum(x[i, w, a, b] for w in range(k)) <= 1,
                name=f"exactly_one_type_i{i}_b{a}_c{b}"
            )


for i in range(N):
    for j in range(k):
        h, w = wymiary_k[j]
        pos = [(a, b) for a in range(Wymiar[0] - h + 1) for b in range(Wymiar[1] - w + 1)]
        for idx1, (a, b) in enumerate(pos):
            model.addConstr(
                gp.quicksum(x[i, j, a+s, b+t] for s in range(h) for t in range(w)) >= h*w * y[i, j, a, b],
                name=f"no_overlap_y_same_obj_j{j}_i{i}_a{a}_b{b}"
                )


for i in range(N):
    for j in range(k):
        h, w = wymiary_k[j]
        pos = [(a, b) for a in range(Wymiar[0] - h + 1) for b in range(Wymiar[1] - w + 1)]
        for idx1, (a, b) in enumerate(pos):
            model.addConstr(
                gp.quicksum(y[i, j, a+s, b+t] for s in range(h) for t in range(w) if (i, j, a+s, b+t) in y) <= 1,
                name=f"no_overlap_y_same_obj_j{j}_i{i}_a{a}_b{b}"
                )


# --- Funkcja celu ---
objective = (gp.quicksum(n[i] for i in range(N)))

model.setObjective(objective, GRB.MINIMIZE)

# --- Rozwiązanie ---
model.optimize()

# --- Wyniki ---
def print_colored_matrix(m):
    color_map = {
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
        for j in range(k):
            h, w = wymiary_k[j]
            for a in range(Wymiar[0]):
                for b in range(Wymiar[1]):
                    key = (i, j, a, b)
                    if key in y and y[key].X > 0.5:
                        for da in range(h):
                            for db in range(w):
                                mat[a + da, b + db] = j+1

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
