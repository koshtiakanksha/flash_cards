from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
french_words_dict = {}

try:
    df = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    french_words_dict = original_data.to_dict(orient="records")
else:
    french_words_dict = df.to_dict(orient="records")
current_card = {}


def generate_new_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(french_words_dict)
    canvas.itemconfigure(title_text, text="French", fill="black")
    canvas.itemconfigure(french_word, text=current_card["French"], fill="black")
    canvas.itemconfigure(card_img, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfigure(card_img, image=card_back_img)
    canvas.itemconfigure(title_text, text="English", fill="white")
    canvas.itemconfigure(french_word, text=current_card["English"], fill="white")


def is_known():
    french_words_dict.remove(current_card)
    data = pandas.DataFrame(french_words_dict)
    data.to_csv("data/words_to_learn.csv", index=False)
    generate_new_word()


window = Tk()
window.title("Flash Card")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
flip_timer = window.after(3000, generate_new_word)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_img = canvas.create_image(400, 263, image=card_front_img)
title_text = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
french_word = canvas.create_text(400, 280, text="word", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=3)

right_button_img = PhotoImage(file="images/right.png")
right_button = Button(height=100, width=100, image=right_button_img, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=2)

wrong_button_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(height=100, width=100, image=wrong_button_img, highlightthickness=0, command=generate_new_word)
wrong_button.grid(row=1, column=0)

generate_new_word()
window.mainloop()
