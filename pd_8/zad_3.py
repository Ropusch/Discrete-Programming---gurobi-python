import gurobipy as gp
from gurobipy import GRB

# ---------------------------------------------------------
# Dane
# ---------------------------------------------------------

widths = [3, 4, 5, 7, 8, 10, 12, 15, 16, 17]
n_types = len(widths)

demand = 2  # każdej wstęgi potrzeba 2 sztuki

# górna granica liczby belek – wystarczy liczba wstęg (=20)
N = n_types * demand

beam_width = 50

# ---------------------------------------------------------
# Model
# ---------------------------------------------------------

m = gp.Model("bin_packing_cutting_stock_bigM")

# ---------------------------------------------------------
# Zmienne
# ---------------------------------------------------------

# binarne: czy belka k jest użyta
use = m.addVars(N, vtype=GRB.BINARY, name="use")

# ile wstęg typu j jest w belce k
x = m.addVars(N, range(n_types), vtype=GRB.INTEGER, lb=0, name="x")

# ---------------------------------------------------------
# Funkcja celu: minimalizacja liczby belek
# ---------------------------------------------------------

m.setObjective(gp.quicksum(use[k] for k in range(N)), GRB.MINIMIZE)

# ---------------------------------------------------------
# Ograniczenia pojemności belki k
# sum_j(width[j] * x[k,j]) <= 50 * use[k]
# ---------------------------------------------------------

for k in range(N):
    m.addConstr(
        gp.quicksum(widths[j] * x[k, j] for j in range(n_types))
        <= beam_width * use[k],
        name=f"capacity_{k}"
    )

# ---------------------------------------------------------
# Zapotrzebowanie – każdej wstęgi >= 2 sztuki
# sum_k x[k,j] >= demand
# ---------------------------------------------------------

for j in range(n_types):
    m.addConstr(
        gp.quicksum(x[k, j] for k in range(N)) >= demand,
        name=f"demand_{j}"
    )

# ---------------------------------------------------------
# Optymalizacja
# ---------------------------------------------------------

m.optimize()

# ---------------------------------------------------------
# Wyniki
# ---------------------------------------------------------

print("\n====== WYNIK ======")
for k in range(N):
    if use[k].x > 0.5:
        print(f"\nBelka {k} użyta:")
        for j in range(n_types):
            if x[k, j].x > 0:
                print(f"  wstęga szerokości {widths[j]}: {int(x[k, j].x)} szt.")
