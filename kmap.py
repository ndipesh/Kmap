import tkinter as tk
from sympy.logic.boolalg import truth_table, SOPform
from sympy.abc import A, B, C, D
from sympy import sympify

# ── Logic ─────────────────────────────────────────────────────────────────────
def get_vars(num_vars):
    return [A, B] if num_vars == 2 else [A, B, C] if num_vars == 3 else [A, B, C, D]

def get_truth_table(expr_str, num_vars):
    variables = get_vars(num_vars)
    expr = sympify(expr_str)
    table = []
    for combo in truth_table(expr, variables):
        inputs = list(combo[0])
        output = int(bool(combo[1]))
        table.append(inputs + [output])
    return table

def minimize(table, num_vars):
    variables = get_vars(num_vars)
    ones = [i for i, row in enumerate(table) if row[-1] == 1]
    if not ones:
        return "0"
    if len(ones) == len(table):
        return "1"
    return str(SOPform(variables, ones))

def solve():
    expr_str = entry.get().strip()
    if not expr_str:
        return
    num_vars = var_choice.get()
    try:
        table = get_truth_table(expr_str, num_vars)
        draw_kmap(table, num_vars)
        minimized = minimize(table, num_vars)
        result_label.config(text=f"Minimized:  {minimized}")
        draw_truth_table(table, num_vars)
    except Exception as e:
        result_label.config(text=f"Error: check your expression")

# ── K-map drawing ─────────────────────────────────────────────────────────────
# Gray code orders for K-map axes
GRAY2 = [0, 1]
GRAY4 = [0, 1, 3, 2]  # 00 01 11 10

def draw_kmap(table, num_vars):
    for widget in kmap_frame.winfo_children():
        widget.destroy()

    if num_vars == 2:
        # Rows: A, Cols: B
        col_labels = ["B=0", "B=1"]
        row_labels = ["A=0", "A=1"]
        # index mapping: A=row, B=col
        def idx(r, c): return r * 2 + c

        tk.Label(kmap_frame, text="", width=6, bg="white").grid(row=0, column=0)
        for c, lbl in enumerate(col_labels):
            tk.Label(kmap_frame, text=lbl, font=("Arial", 11, "bold"),
                     bg="white", width=8).grid(row=0, column=c+1)
        for r, lbl in enumerate(row_labels):
            tk.Label(kmap_frame, text=lbl, font=("Arial", 11, "bold"),
                     bg="white", width=6).grid(row=r+1, column=0)
            for c in range(2):
                val = table[idx(r, c)][-1]
                color = "#90EE90" if val == 1 else "#FFB6C1"
                tk.Label(kmap_frame, text=str(val), width=8, height=2,
                         font=("Arial", 14, "bold"),
                         bg=color, relief="solid", borderwidth=1).grid(
                         row=r+1, column=c+1, padx=3, pady=3)

    elif num_vars == 3:
        # Rows: A,  Cols: BC in Gray order 00 01 11 10
        col_labels = ["BC=00", "BC=01", "BC=11", "BC=10"]
        row_labels = ["A=0", "A=1"]
        gray_cols = GRAY4[:4]  # BC: 0,1,3,2

        tk.Label(kmap_frame, text="", width=7, bg="white").grid(row=0, column=0)
        for c, lbl in enumerate(col_labels):
            tk.Label(kmap_frame, text=lbl, font=("Arial", 10, "bold"),
                     bg="white", width=7).grid(row=0, column=c+1)
        for r in range(2):
            tk.Label(kmap_frame, text=row_labels[r], font=("Arial", 11, "bold"),
                     bg="white", width=7).grid(row=r+1, column=0)
            for c, bc in enumerate(gray_cols):
                # minterm index: A*4 + BC
                minterm = r * 4 + bc
                val = table[minterm][-1]
                color = "#90EE90" if val == 1 else "#FFB6C1"
                tk.Label(kmap_frame, text=str(val), width=7, height=2,
                         font=("Arial", 14, "bold"),
                         bg=color, relief="solid", borderwidth=1).grid(
                         row=r+1, column=c+1, padx=3, pady=3)

    elif num_vars == 4:
        # Rows: AB in Gray order, Cols: CD in Gray order
        ab_labels = ["AB=00", "AB=01", "AB=11", "AB=10"]
        cd_labels = ["CD=00", "CD=01", "CD=11", "CD=10"]

        tk.Label(kmap_frame, text="", width=7, bg="white").grid(row=0, column=0)
        for c, lbl in enumerate(cd_labels):
            tk.Label(kmap_frame, text=lbl, font=("Arial", 10, "bold"),
                     bg="white", width=7).grid(row=0, column=c+1)
        for r, ab in enumerate(GRAY4):
            tk.Label(kmap_frame, text=ab_labels[r], font=("Arial", 10, "bold"),
                     bg="white", width=7).grid(row=r+1, column=0)
            for c, cd in enumerate(GRAY4):
                minterm = ab * 4 + cd
                val = table[minterm][-1]
                color = "#90EE90" if val == 1 else "#FFB6C1"
                tk.Label(kmap_frame, text=str(val), width=7, height=2,
                         font=("Arial", 13, "bold"),
                         bg=color, relief="solid", borderwidth=1).grid(
                         row=r+1, column=c+1, padx=2, pady=2)

def draw_truth_table(table, num_vars):
    for widget in tt_frame.winfo_children():
        widget.destroy()
    var_names = ["A", "B"] if num_vars == 2 else \
                ["A", "B", "C"] if num_vars == 3 else ["A", "B", "C", "D"]
    headers = var_names + ["Output"]
    for j, h in enumerate(headers):
        tk.Label(tt_frame, text=h, font=("Arial", 11, "bold"),
                 bg="white", width=6).grid(row=0, column=j, padx=2)
    for i, row in enumerate(table):
        shade = "#f0f0f0" if i % 2 == 0 else "white"
        for j, val in enumerate(row):
            tk.Label(tt_frame, text=str(val), font=("Arial", 11),
                     bg=shade, width=6).grid(row=i+1, column=j, padx=2)

# ── Window ────────────────────────────────────────────────────────────────────
window = tk.Tk()
window.title("Karnaugh Map Solver")
window.geometry("620x700")
window.configure(bg="white")

tk.Label(window, text="Karnaugh Map Solver",
         font=("Arial", 20, "bold"), bg="white").pack(pady=10)

# ── Variable selector ─────────────────────────────────────────────────────────
var_frame = tk.Frame(window, bg="white")
var_frame.pack(pady=5)
tk.Label(var_frame, text="Variables:", font=("Arial", 12),
         bg="white").pack(side="left", padx=5)
var_choice = tk.IntVar(value=2)
for n, label in [(2, "2 vars (A,B)"), (3, "3 vars (A,B,C)"), (4, "4 vars (A,B,C,D)")]:
    tk.Radiobutton(var_frame, text=label, variable=var_choice, value=n,
                   font=("Arial", 11), bg="white").pack(side="left", padx=5)

# ── Input ─────────────────────────────────────────────────────────────────────
input_frame = tk.Frame(window, bg="white")
input_frame.pack(pady=5)
tk.Label(input_frame, text="Expression:", font=("Arial", 12),
         bg="white").grid(row=0, column=0, padx=5)
entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
entry.grid(row=0, column=1, padx=5)
entry.insert(0, "A & B | ~A & ~B")
tk.Button(input_frame, text="Solve", font=("Arial", 12, "bold"),
          bg="#4CAF50", fg="white", command=solve).grid(row=0, column=2, padx=5)

tk.Label(window, text="Use:  & = AND   | = OR   ~ = NOT",
         font=("Arial", 10), bg="white", fg="gray").pack()

# ── K-map ─────────────────────────────────────────────────────────────────────
tk.Label(window, text="K-Map", font=("Arial", 14, "bold"),
         bg="white").pack(pady=(10, 0))
kmap_frame = tk.Frame(window, bg="white")
kmap_frame.pack(pady=5)

# ── Result ────────────────────────────────────────────────────────────────────
result_label = tk.Label(window, text="Minimized:  —",
                        font=("Arial", 13, "bold"),
                        bg="#e8f5e9", fg="#2e7d32",
                        relief="solid", padx=10, pady=8)
result_label.pack(pady=10, padx=20, fill="x")

# ── Truth table ───────────────────────────────────────────────────────────────
tk.Label(window, text="Truth Table", font=("Arial", 14, "bold"),
         bg="white").pack()
tt_frame = tk.Frame(window, bg="white")
tt_frame.pack(pady=5)

solve()
window.mainloop()