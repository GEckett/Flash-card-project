BACKGROUND_COLOR = "#B1DDC6"
LANG_FONT = ("Ariel", 40, "italic")
WORD_FONT = ("Ariel", 60, "italic")
from tkinter import *
import pandas
import random

#------------------------- Data --------------------------------#
word = {}
try:
    words = pandas.read_csv("./data/Words_to_learn.csv")
except FileNotFoundError:
    original_words = pandas.read_csv("./data/french_words.csv")
    word_dict = original_words.to_dict(orient="records")
else:
    word_dict = words.to_dict(orient="records")



#--------------------- Random French ---------------------------#

def next_card():
    canvas.itemconfig(card_side, image=card_front)
    global word, flip_time
    window.after_cancel(flip_time)
    word = random.choice(word_dict)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_text, text=word["French"], fill="black")
    window.after(3000, func=card_flip)


#------------------------Card Flip -----------------------------#

def card_flip():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_text, text=word["English"], fill="white")
    canvas.itemconfig(card_side, image=card_back)


#----------------------- Remove Word ---------------------------#


def remove_word():
    word_dict.remove(word)
    next_card()
    data = pandas.DataFrame(word_dict)
    data.to_csv("./data/Words_to_learn.csv", index=False)


#------------------------- UI ----------------------------------#

window = Tk()
window.title("French Flash Cards")
window.wm_minsize(width=850, height=576,)
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_time = window.after(3000, func=card_flip)

canvas = Canvas(bg=BACKGROUND_COLOR, highlightthickness=0, height=526, width=800)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
card_side = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, text="Title", font=LANG_FONT)
card_text = canvas.create_text(400, 263, text="Word", font=WORD_FONT)
canvas.grid(row=0, column=0, columnspan=2)

right_but_img = PhotoImage(file="./images/right.png")
right_but = Button(image=right_but_img, highlightthickness=0, command=remove_word)
right_but.grid(row=1, column=0)

wrong_but_img = PhotoImage(file="./images/wrong.png")
wrong_but = Button(image=wrong_but_img, highlightthickness=0, command=next_card)
wrong_but.grid(row=1, column=1)


next_card()


window.mainloop()