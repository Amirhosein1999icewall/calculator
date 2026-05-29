import tkinter as tk
import tkinter.font as font

# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("Calculator")
root.geometry("320x500")
root.resizable(False, False)

# ---------------- COLORS ----------------
BG_COLOR = "#2c3e50"
ENTRY_BG = "#34495e"

BUTTON_FG = "#ecf0f1"

BUTTON_BG_NUM = "#4a627a"
BUTTON_BG_OP = "#3498db"
BUTTON_BG_EQUAL = "#e67e22"
BUTTON_BG_CLEAR = "#e74c3c"
BUTTON_BG_DEL = "#f39c12"

root.config(bg=BG_COLOR)

# ---------------- FONTS ----------------
try:
    button_font = font.Font(family='Arial Rounded MT Bold', size=14)
    entry_font = font.Font(family='Arial Rounded MT Bold', size=22)
except:
    button_font = font.Font(size=14, weight="bold")
    entry_font = font.Font(size=22, weight="bold")

# ---------------- DISPLAY ----------------
entry_var = tk.StringVar()

entry = tk.Entry(
    root,
    textvariable=entry_var,
    font=entry_font,
    justify="right",
    bd=0,
    bg=ENTRY_BG,
    fg=BUTTON_FG,
    insertbackground="white"
)

entry.grid(row=0, column=0, columnspan=4,
           padx=10, pady=20, ipady=15, sticky="nsew")

# ---------------- VARIABLES ----------------
expression = ""
result_shown = False

# ---------------- FUNCTIONS ----------------
def press(value):
    global expression, result_shown

    operators = ['+', '-', '*', '/']

    # اگر نتیجه نمایش داده شده و کاربر عدد زد
    if result_shown and value not in operators:
        expression = ""
        result_shown = False

    # جلوگیری از چند عملگر پشت سر هم
    if expression:
        if expression[-1] in operators and value in operators:
            expression = expression[:-1]

    # جلوگیری از چند اعشار در یک عدد
    if value == '.':
        parts = expression.split()
        last = parts[-1] if parts else ""

        if '.' in last:
            return

        if last == "" or last in operators:
            expression += "0"

    expression += str(value)

    entry_var.set(expression)


def equalpress():
    global expression, result_shown

    try:
        result = str(eval(expression))
        entry_var.set(result)
        expression = result
        result_shown = True

    except ZeroDivisionError:
        entry_var.set("Cannot divide by zero")
        expression = ""

    except:
        entry_var.set("Error")
        expression = ""


def clear():
    global expression
    expression = ""
    entry_var.set("")


def backspace():
    global expression

    if expression:
        expression = expression[:-1]
        entry_var.set(expression)


# ---------------- BUTTON FRAME ----------------
button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.grid(row=1, column=0, columnspan=4,
                  padx=5, pady=5, sticky="nsew")

for i in range(5):
    button_frame.grid_rowconfigure(i, weight=1)

for i in range(4):
    button_frame.grid_columnconfigure(i, weight=1)

# ---------------- BUTTONS ----------------
buttons = [

    ('C', 0, 0, BUTTON_BG_CLEAR, clear),
    ('DEL', 0, 1, BUTTON_BG_DEL, backspace),
    ('/', 0, 2, BUTTON_BG_OP, lambda: press('/')),
    ('*', 0, 3, BUTTON_BG_OP, lambda: press('*')),

    ('7', 1, 0, BUTTON_BG_NUM, lambda: press('7')),
    ('8', 1, 1, BUTTON_BG_NUM, lambda: press('8')),
    ('9', 1, 2, BUTTON_BG_NUM, lambda: press('9')),
    ('-', 1, 3, BUTTON_BG_OP, lambda: press('-')),

    ('4', 2, 0, BUTTON_BG_NUM, lambda: press('4')),
    ('5', 2, 1, BUTTON_BG_NUM, lambda: press('5')),
    ('6', 2, 2, BUTTON_BG_NUM, lambda: press('6')),
    ('+', 2, 3, BUTTON_BG_OP, lambda: press('+')),

    ('1', 3, 0, BUTTON_BG_NUM, lambda: press('1')),
    ('2', 3, 1, BUTTON_BG_NUM, lambda: press('2')),
    ('3', 3, 2, BUTTON_BG_NUM, lambda: press('3')),
    ('=', 3, 3, BUTTON_BG_EQUAL, equalpress),

    ('0', 4, 0, BUTTON_BG_NUM, lambda: press('0')),
    ('.', 4, 2, BUTTON_BG_NUM, lambda: press('.')),
]

# ---------------- CREATE BUTTONS ----------------
for (text, row, col, color, command) in buttons:

    colspan = 2 if text == '0' else 1
    rowspan = 2 if text == '=' else 1

    btn = tk.Button(
        button_frame,
        text=text,
        bg=color,
        fg="white",
        font=button_font,
        bd=0,
        relief="flat",
        activebackground="#95a5a6",
        activeforeground="white",
        command=command,
        cursor="hand2"
    )

    btn.grid(
        row=row,
        column=col,
        columnspan=colspan,
        rowspan=rowspan,
        padx=4,
        pady=4,
        sticky="nsew"
    )

# ---------------- KEYBOARD SUPPORT ----------------
root.bind('<Return>', lambda event: equalpress())
root.bind('<BackSpace>', lambda event: backspace())

for key in "0123456789+-*/.":
    root.bind(key, lambda event, k=key: press(k))

# ---------------- GRID CONFIG ----------------
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# ---------------- START ----------------
root.mainloop()
