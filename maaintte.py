import tkinter as tk

LEVELS = {
    "Базовый": (1, ["math", "random", "datetime", "os", "sys"]),
    "Средний": (2, ["json", "re", "collections", "requests", "tkinter", "sqlite3"]),
    "Продвинутый": (3, ["numpy", "pandas", "matplotlib", "flask", "pytest", "beautifulsoup4"]),
    "Экспертный": (4, ["django", "scikit-learn", "pytorch", "tensorflow", "asyncio", "fastapi"]),
}

MAX_SCORE = sum(weight * len(libs) for weight, libs in LEVELS.values())


def get_score():
    score = 0
    for group, (weight, libs) in LEVELS.items():
        for lib in libs:
            if variables[lib].get():
                score += weight
    return score


def get_level_name(score):
    if score == 0:
        return "Ты только в начале пути"
    elif score < 8:
        return "Новичок"
    elif score < 20:
        return "Начинающий"
    elif score < 35:
        return "Средний уровень"
    elif score < 50:
        return "Продвинутый"
    else:
        return "Эксперт"


def check_level():
    name = entry_name.get().strip()
    if name == "":
        name = "Друг"

    score = get_score()
    level = get_level_name(score)
    percent = round(score / MAX_SCORE * 100)

    result = (
        f"{name}, твой уровень: {level}\n"
        f"Баллов: {score} из {MAX_SCORE} ({percent}%)"
    )

    result_label.config(text=result)

    if percent < 100:
        next_button.pack(pady=5)
    else:
        next_button.pack_forget()


def next_steps():
    name = entry_name.get().strip()
    if name == "":
        name = "Друг"

    result = f"Что изучить дальше, {name}:\n\n"
    found = 0

    for group, (weight, libs) in LEVELS.items():
        for lib in libs:
            if not variables[lib].get() and found < 3:
                result += f"• {lib} (уровень: {group})\n"
                found += 1

    result_label.config(text=result)


window = tk.Tk()
window.title("Твой уровень Python")
window.geometry("720x620")

tk.Label(window, text="Твоё имя:").pack()

entry_name = tk.Entry(window)
entry_name.pack()

tk.Label(
    window,
    text="Отметь библиотеки, которые ты знаешь и использовал(а):"
).pack(pady=8)

variables = {}

frame = tk.Frame(window)
frame.pack()

for column, (group, (weight, libs)) in enumerate(LEVELS.items()):
    tk.Label(
        frame,
        text=group,
        font=("Arial", 10, "bold")
    ).grid(row=0, column=column, padx=15, pady=5)

    for row, lib in enumerate(libs, start=1):
        variables[lib] = tk.BooleanVar()
        tk.Checkbutton(
            frame,
            text=lib,
            variable=variables[lib]
        ).grid(row=row, column=column, sticky="w", padx=15)

button = tk.Button(
    window,
    text="Узнать уровень",
    command=check_level
)
button.pack(pady=10)

result_label = tk.Label(window, text="", justify="left")
result_label.pack()

next_button = tk.Button(
    window,
    text="Что изучить дальше",
    command=next_steps
)

window.mainloop()