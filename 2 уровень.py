#%%
import os
import tkinter as tk
import random


# Папка с картинками лежит рядом с этим файлом
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def img_path(name):
    return os.path.join(BASE_DIR, "img", name)


# Окно
root = tk.Tk()
root.title("Собери яблоки на благо страны")

WIDTH = 600
HEIGHT = 600

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT
)
canvas.pack()


# Картинки (ссылки на PhotoImage нужно хранить в переменных,
# иначе tkinter их "потеряет" и картинки не покажутся)
bg_image = tk.PhotoImage(file=img_path("tree.png"))
# tree.png 400x400 -> растягиваем до 600x600 (x3, потом /2)
bg_image = bg_image.zoom(3).subsample(2)

basket_image = tk.PhotoImage(file=img_path("basket.png"))

images = {
    "apple": tk.PhotoImage(file=img_path("apple.png")),
    "pear": tk.PhotoImage(file=img_path("pear.png")),
    "trash": tk.PhotoImage(file=img_path("can.png")),
    "bomb": tk.PhotoImage(file=img_path("bomb.png")),
}

# Фон
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

basket = canvas.create_image(
    basket_x,
    basket_y,
    image=basket_image
)


# Падающие предметы
objects = []


# Создание предмета: яблоко, груша, банка или бомба
def create_object():
    if not game_active:
        return

    x = random.randint(30, 570)
    y = 50

    number = random.randint(1, 10)

    if number <= 2:
        object_type = "trash"   # банка (20%)
    elif number == 3:
        object_type = "bomb"    # бомба (10%)
    elif number <= 5:
        object_type = "pear"    # груша (20%)
    else:
        object_type = "apple"   # яблоко (50%)

    item = canvas.create_image(
        x,
        y,
        image=images[object_type]
    )

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

    if game_active and basket_x < 570:
        basket_x += 20
        canvas.move(basket, 20, 0)


# Обновление счёта на экране
def update_score_text():
    canvas.itemconfig(
        score_text,
        text=f"Счёт: {score}"
    )


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

        if not game_active:
            break

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
                    update_score_text()

                elif object_type == "pear":
                    score += 2
                    update_score_text()

                elif object_type == "bomb":
                    # Бомба: -2 очка (ниже нуля не уходим) и -1 жизнь
                    score = max(0, score - 2)
                    update_score_text()
                    lose_life()

                else:
                    lose_life()

                canvas.delete(item)
                objects.remove(obj)

                continue

        # Если предмет упал мимо
        if y > HEIGHT:

            # Мимо упали яблоко или груша - минус жизнь
            if object_type == "apple" or object_type == "pear":
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
        text="Игра оконченааППАХАхАХХХАХХА!",
        font=("Arial", 24, "bold")
    )

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2 + 20,
        text=f"Ты набрал {score} очков лол",
        font=("Arial", 16)
    )


# Управление
root.bind("<Left>", move_left)
root.bind("<Right>", move_right)


# Запуск игры
create_object()
update_game()

root.mainloop()
