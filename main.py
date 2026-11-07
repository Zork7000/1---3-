import tkinter as tk
import random


# Окно
root = tk.Tk()
root.title("Собери урожай")

WIDTH = 400
HEIGHT = 400

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT
)
canvas.pack()


# Фон
bg_image = tk.PhotoImage(file="img/tree.png")
bg_id = canvas.create_image(
    0,
    0,
    image=bg_image,
    anchor="nw"
)


# Счёт и жизни
score = 0
lives = 3
game_active = True

score_text = canvas.create_text(
    50,
    20,
    text="Счёт: 0",
    font=("Arial", 14)
)

lives_text = canvas.create_text(
    330,
    20,
    text="❤️❤️❤️",
    font=("Arial", 14),
    fill="red"
)


# Корзинка
basket_x = 200
basket_y = 350

basket = canvas.create_text(
    basket_x,
    basket_y,
    text="🧺",
    font=("Arial", 35),
    fill="brown"
)


# Падающие предметы
objects = []


# Создание яблока или мусора
def create_object():
    if not game_active:
        return

    x = random.randint(30, 370)
    y = 50

    if random.randint(1, 5) == 1:
        item = canvas.create_text(
            x,
            y,
            text="🥫",
            font=("Arial", 25),
            fill="red"
        )
        object_type = "trash"
    else:
        item = canvas.create_text(
            x,
            y,
            text="🍎",
            font=("Arial", 25),
            fill="red"
        )
        object_type = "apple"

    objects.append([item, x, y, object_type])

    root.after(1000, create_object)


# Движение корзинки
def move_left(event):
    global basket_x

    if game_active and basket_x > 30:
        basket_x -= 20
        canvas.move(basket, -20, 0)


def move_right(event):
    global basket_x

    if game_active and basket_x < 370:
        basket_x += 20
        canvas.move(basket, 20, 0)


# Потеря жизни
def lose_life():
    global lives, game_active

    lives -= 1

    canvas.itemconfig(
        lives_text,
        text="❤️" * lives
    )

    if lives <= 0:
        game_active = False
        end_game()


# Игровой цикл
def update_game():
    global score

    if not game_active:
        return

    for obj in objects[:]:

        item = obj[0]
        x = obj[1]
        y = obj[2]
        object_type = obj[3]

        # Двигаем предмет вниз
        y += 5
        obj[2] = y

        canvas.move(item, 0, 5)

        # Проверяем, поймали ли предмет
        if y >= 330 and y <= 370:

            if abs(x - basket_x) < 40:

                if object_type == "apple":
                    score += 1

                    canvas.itemconfig(
                        score_text,
                        text=f"Счёт: {score}"
                    )

                else:
                    lose_life()

                canvas.delete(item)
                objects.remove(obj)

                continue

        # Если яблоко упало мимо
        if y > HEIGHT:

            if object_type == "apple":
                lose_life()

            canvas.delete(item)
            objects.remove(obj)

    if game_active:
        root.after(50, update_game)


# Конец игры
def end_game():
    canvas.delete("all")

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2 - 30,
        text="УРОЖАЙ СОБРАН!",
        font=("Arial", 24, "bold")
    )

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2 + 20,
        text=f"Ты набрал {score} очков",
        font=("Arial", 16)
    )


# Управление
root.bind("<Left>", move_left)
root.bind("<Right>", move_right)


# Запуск игры
create_object()
update_game()

root.mainloop()