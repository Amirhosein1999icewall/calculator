import tkinter as tk
import tkinter.font as font
from tkinter import ttk

# --- تنظیمات کلی ---
root = tk.Tk()
root.title("calculator")
root.geometry("320x500") # کمی بزرگتر برای جا دادن دکمه ها
root.resizable(False, False)

# --- رنگ‌ها ---
BG_COLOR = "#2c3e50"       # پس‌زمینه کلی (تیره)
ENTRY_BG = "#34495e"       # پس‌زمینه صفحه نمایش
BUTTON_FG_TEXT = "#ecf0f1" # رنگ متن دکمه های عددی (روشن)
BUTTON_FG_WHITE = "#ffffff" # رنگ متن دکمه های خاص (مثل =)

BUTTON_BG_NUMBERS = "#4a627a"      # رنگ دکمه های عددی (خاکستری تیره)
BUTTON_BG_OPERATOR = "#3498db"     # رنگ دکمه های عملیاتی (آبی)
BUTTON_BG_EQUALS = None            # رنگ دکمه مساوی (از گرادینت استفاده می شود)
BUTTON_BG_CLEAR = "#e74c3c"        # رنگ دکمه پاک کردن (قرمز)
BUTTON_BG_DEL = "#f39c12"          # رنگ دکمه DEL (نارنجی)
BUTTON_BG_OPERATOR_RIGHT = "#3498db" # رنگ دکمه های عملیاتی سمت راست

# --- فونت سفارشی ---
try:
    # فونت شبیه به تصویر (اگر موجود نباشد، از فونت پیش فرض استفاده می شود)
    button_font = font.Font(family='Arial Rounded MT Bold', size=14)
    entry_font = font.Font(family='Arial Rounded MT Bold', size=20)
except:
    button_font = font.Font(family='Helvetica', size=14, weight='bold')
    entry_font = font.Font(family='Helvetica', size=20)

# --- تنظیم رنگ پس‌زمینه پنجره ---
root.config(bg=BG_COLOR)

# --- ورودی اصلی نمایش اعداد و نتایج ---
entry_var = tk.StringVar()
entry = tk.Entry(root, textvariable=entry_var, font=entry_font, bd=0, insertwidth=2, width=14, justify='right', bg=ENTRY_BG, fg=BUTTON_FG_TEXT, insertbackground=BUTTON_FG_TEXT)
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=25, ipady=10, sticky="nsew")

# --- متغیرها ---
expression = ""

# --- توابع ---
def press(num):
    global expression
    if entry_var.get() == "Error":
        expression = ""
        entry_var.set("")
    # جلوگیری از ورود چند صفر پشت سر هم در ابتدای ورودی
    if expression == "0" and num == '0':
        return
    # جلوگیری از ورود چند علامت اعشار پشت سر هم
    if num == '.' and '.' in expression.split(' ')[-1]: # بررسی آخرین بخش عدد
         return
    # جلوگیری از ورود چند عملگر پشت سر هم (به جز وقتی که عملگر قبلی جابجا شده)
    operators = ['+', '-', '*', '/']
    if num in operators and expression and expression[-1] in operators:
        # اگر عملگر قبلی جدا بود، آن را حذف کن
        if expression.count(' ') == 0: # اگر هنوز space نداریم یعنی فقط یک عدد بوده
             expression = expression[:-1]
        else: # اگر space داریم یعنی عدد قبلی کامل شده
             parts = expression.split(' ')
             if len(parts) > 1 and parts[-1] == '': # اگر عملگر قبلی در انتها بوده
                  expression = ' '.join(parts[:-2]) + ' ' # حذف عدد قبلی و عملگر قبلی

    expression += str(num)
    entry_var.set(expression)


def equalpress():
    global expression
    try:
        # نمایش فرمت ورودی قبل از محاسبه
        formatted_expression = expression.replace('/', ' ÷ ').replace('*', ' × ').replace('-', ' - ').replace('+', ' + ')
        entry_var.set(formatted_expression)

        # محاسبه نهایی
        total = str(eval(expression))
        entry_var.set(total)
        expression = total
    except ZeroDivisionError:
        entry_var.set("Error")
        expression = ""
    except Exception as e:
        # نمایش نوع خطا برای اشکال زدایی
        # print(f"Error: {e}")
        entry_var.set("Error")
        expression = ""

def clear():
    global expression
    expression = ""
    entry_var.set("")

def backspace():
    global expression
    if expression and entry_var.get() != "Error":
        expression = expression[:-1]
        entry_var.set(expression)

# --- فریم برای دکمه‌ها ---
button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

# تنظیم وزن برای سطر و ستون‌های داخل فریم
for i in range(5): # 5 سطر اصلی دکمه ها
    button_frame.grid_rowconfigure(i, weight=1)
for i in range(4): # 4 ستون اصلی
    button_frame.grid_columnconfigure(i, weight=1)

# --- تعریف دکمه‌ها بر اساس تصویر ---
# (متن, سطر, ستون, رنگ پس‌زمینه, رنگ متن, دستور, rowspan, columnspan, custom_bg_gradient)
buttons_config = [
    # ردیف اول
    ('C', 0, 0, BUTTON_BG_CLEAR, BUTTON_FG_WHITE, clear, 1, 1, None),
    ('DEL', 0, 1, BUTTON_BG_DEL, BUTTON_FG_WHITE, backspace, 1, 1, None),
    ('+', 0, 2, BUTTON_BG_OPERATOR, BUTTON_FG_TEXT, lambda: press('+'), 1, 1, None),
    ('*', 0, 3, BUTTON_BG_OPERATOR, BUTTON_FG_TEXT, lambda: press('*'), 1, 1, None),

    # ردیف دوم
    ('7', 1, 0, BUTTON_BG_NUMBERS, BUTTON_FG_TEXT, lambda: press('7'), 1, 1, None),
    ('8', 1, 1, BUTTON_BG_NUMBERS, BUTTON_FG_TEXT, lambda: press('8'), 1, 1, None),
    ('9', 1, 2, BUTTON_BG_NUMBERS, BUTTON_FG_TEXT, lambda: press('9'), 1, 1, None),
    ('-', 1, 3, BUTTON_BG_OPERATOR, BUTTON_FG_TEXT, lambda: press('-'), 1, 1, None),

    # ردیف سوم
    ('4', 2, 0, BUTTON_BG_NUMBERS, BUTTON_FG_TEXT, lambda: press('4'), 1, 1, None),
    ('5', 2, 1, BUTTON_BG_NUMBERS, BUTTON_FG_TEXT, lambda: press('5'), 1, 1, None),
    ('6', 2, 2, BUTTON_BG_NUMBERS, BUTTON_FG_TEXT, lambda: press('6'), 1, 1, None),
    ('+', 2, 3, BUTTON_BG_OPERATOR_RIGHT, BUTTON_FG_TEXT, lambda: press('+'), 1, 1, None), # + در سمت راست

    # ردیف چهارم
    ('1', 3, 0, BUTTON_BG_NUMBERS, BUTTON_FG_TEXT, lambda: press('1'), 1, 1, None),
    ('2', 3, 1, BUTTON_BG_NUMBERS, BUTTON_FG_TEXT, lambda: press('2'), 1, 1, None),
    ('3', 3, 2, BUTTON_BG_NUMBERS, BUTTON_FG_TEXT, lambda: press('3'), 1, 1, None),
    ('=', 3, 3, None, BUTTON_FG_WHITE, equalpress, 2, 1, ("#ff758c", "#ffa647")), # گرادینت برای مساوی

    # ردیف پنجم
    ('0', 4, 0, BUTTON_BG_NUMBERS, BUTTON_FG_TEXT, lambda: press('0'), 1, 2, None), # صفر عرض دو برابر
    ('.', 4, 2, BUTTON_BG_NUMBERS, BUTTON_FG_TEXT, lambda: press('.'), 1, 1, None),
]

# --- ایجاد دکمه‌ها ---
buttons = {}
for text, row, col, bg_color, fg_color, cmd, rowspan, columnspan, custom_gradient in buttons_config:
    button_options = {
        "text": text, "fg": fg_color, "font": button_font,
        "command": cmd, "relief": tk.RAISED, "bd": 0 # بدون border برای ظاهر بهتر
    }
    if custom_gradient:
        # برای دکمه مساوی که گرادینت دارد
        button = tk.Button(button_frame, **button_options)
        # Tkinter مستقیماً گرادینت را پشتیبانی نمی‌کند، پس از یک ترفند استفاده می‌کنیم
        # یا اینکه یک تصویر گرادینت ایجاد کنیم یا رنگ را در زمان فشردن تغییر دهیم
        # در اینجا از رنگ ثابت استفاده می‌کنیم و گرادینت فقط در صورت نیاز و با پیچیدگی بیشتر قابل پیاده‌سازی است
        # برای سادگی، از رنگ میانه گرادینت استفاده می‌کنیم یا یکی از رنگ‌ها
        button.config(bg="#e08d72") # رنگ میانه صورتی/نارنجی
    else:
        button_options["bg"] = bg_color
        button = tk.Button(button_frame, **button_options)

    button.grid(row=row, column=col, columnspan=columnspan, rowspan=rowspan, padx=4, pady=4, sticky="nsew")
    buttons[text] = button # ذخیره دکمه برای دسترسی بعدی

    # افکت فشردن دکمه (تغییر رنگ جزئی)
    original_bg = button.cget("bg")
    button.bind("<ButtonPress-1>", lambda e, btn=button, bg=original_bg: btn.config(bg="#d0d0d0" if btn.cget("text") not in ['C', 'DEL'] else "#a0a0a0"))
    button.bind("<ButtonRelease-1>", lambda e, btn=button, bg=original_bg: btn.config(bg=bg))


# --- تنظیمات grid اصلی پنجره ---
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1) # فریم دکمه‌ها باید فضا را پر کند

# --- اتصال کلید Enter به تابع equalpress ---
root.bind('<Return>', lambda event=None: equalpress())

# --- اتصال کلید Backspace برای پاک کردن ---
root.bind('<BackSpace>', lambda event=None: backspace())

# --- اتصال کلیدهای عددی و عملیاتی ---
for char_code in range(48, 58): # 0-9
    root.bind(chr(char_code), lambda event, num=chr(char_code): press(num))
for char_code in [42, 43, 45, 47]: # *, +, -, /
    root.bind(chr(char_code), lambda event, num=chr(char_code): press(num))
root.bind('.', lambda event: press('.'))

# --- تنظیمات نهایی ---
# تنظیم رنگ گرادینت برای دکمه مساوی (نیاز به کد پیچیده‌تر برای گرادینت واقعی دارد)
# در اینجا فقط از رنگ ثابت استفاده شده است
# برای پیاده‌سازی واقعی گرادینت، نیاز به استفاده از Pillow و Canvas Tkinter است

root.mainloop()

