BACKGROUND_COLOR = "#B1DDC6"
from tkinter import *
import pandas
import random
import csv

window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

#We need the white surface pic in the middle
#Canvas
white_canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
front_image = white_canvas.create_image(410, 270, image=card_front)

#Creating text on top of canvas
language = white_canvas.create_text(420, 150, text="French", font=("Ariel", 40, "italic"))
word = white_canvas.create_text(410, 270, text="text", font=("Ariel", 50, "bold"))

white_canvas.grid(column=0, row=0, columnspan=2)

try:
   data = pandas.read_csv("./data/words_to_learn.csv.csv")
except FileNotFoundError:
    data = pandas.read_csv("./data/french_words.csv")

list_of_dict = data.to_dict(orient="records")  #creates a list that has each dictionary containing the French and English
current_card = {}


def flip_card():
    white_canvas.itemconfig(front_image, image=card_back)
    white_canvas.itemconfig(language, text="English", fill="white")
    white_canvas.itemconfig(word, text=current_card['English'], fill="white")


#once pressed, the check_button retrives the french word from the csv and configs it to the word on the canvas
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)  #stop the timer if we want to skip words and not have the 3s running

    #check the unknown.csv file
    #if the file has not been created yet, retrieve from french_words

    current_card = random.choice(list_of_dict)  # individual dictionary with English translation and French word

    white_canvas.itemconfig(front_image, image=card_front)
    white_canvas.itemconfig(language, text="French", fill="black")
    white_canvas.itemconfig(word, text=current_card["French"], fill="black")


    flip_timer = window.after(3000, lambda: flip_card())  #start the timer here again #call to flip card for English translation
    #lambda causes it to wait for 3 seconds and not call the function immediately

def known_card():
    list_of_dict.remove(current_card)
    data = pandas.DataFrame(list_of_dict)
    data.to_csv("data/words_to_learn.csv")

    next_card()


#Button Images (Cross and Check)
cross_image = PhotoImage(file="./images/wrong.png")
cross = Button(image=cross_image, command=next_card)
check_image = PhotoImage(file="./images/right.png")
check = Button(image=check_image, command=known_card)

cross.grid(column=0, row=1)
check.grid(column=1, row=1)

flip_timer = window.after(3000, lambda: flip_card())
next_card()
window.mainloop()
