import random as random
from tkinter import Tk
from wordleGUI import Mordle

class Main:
    def __init__(self):
        return
    
    def pick_word():
        word_file_path = 'MORDLE\Training_Data\shuffled_data.txt'
        with open(word_file_path) as file:
            wordList = file.readlines()
        wordList = [word.strip() for word in wordList]
        return random.choice(wordList).lower()

    root = Tk()
    root.geometry("900x1000")
    start = Mordle(root, pick_word())
    root.mainloop()  
        