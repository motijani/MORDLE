from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import os
import random

stage_bg = "#171717"  # A very dark grey

class Mordle:
    def __init__(self, root):
        self.root = root
        self.guess_row = 0
        self.canvas_width = 350
        self.canvas_height = 400
        self.updating_row = False
        self.update_speed = 0
        self.word_guess = [
            ['', '', '', '', ''],
            ['', '', '', '', ''],
            ['', '', '', '', ''],
            ['', '', '', '', ''],
            ['', '', '', '', '']
        ]
        self.sol_word = self.pick_word()
        print(self.sol_word)
        self.boxes = []
        self.image_list = []
        self.letterImages = []
        self.create_title()
        self.word_disp = Canvas(self.root,width=self.canvas_width, height=self.canvas_height, bg='#1d1d1d', bd = 2, relief='solid', highlightbackground='#333333')
        self.word_disp.pack()
        self.create_grid()
        self.root.configure(background=stage_bg)
        self.root.bind('<KeyPress>', self.onKeyPress)
    def pick_word(self):
        __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))) # Getting current file directory
        word_file_path = os.path.join(__location__,'Training_Data','shuffled_data.txt')
        with open(word_file_path) as file:
            wordList = file.readlines()
        wordList = [word.strip() for word in wordList]
        return random.choice(wordList).lower()
    def create_grid(self):
        box_size = 70
        box_size = 65
        grid_width = 5
        grid_height = 5

        # Calculate the total width and height of the grid
        grid_total_width = box_size * grid_width
        grid_total_height = box_size * grid_height

        # Calculate the offset to center the grid within the canvas
        offset_x = ((self.canvas_width - grid_total_width) // 2) + 3
        offset_y = ((self.canvas_height - grid_total_height) // 2) + 5
        for i in range(5):
            row = []
            for j in range(5):
                x1 = offset_x + j * box_size
                y1 = offset_y + i * box_size
                x2 = x1 + box_size
                y2 = y1 + box_size
                rect_id = self.word_disp.create_rectangle(x1, y1, x2, y2, fill='#1d1d1d', outline='black', width=3)
                row.append(rect_id)
            self.boxes.append(row)      
    def create_title(self):
        title_label = Label(self.root, text="MORDLE", pady=5, fg="white", bg=stage_bg,
                            font=("Lucida Sans", 35, "bold"))
        title_label.pack()
        cstm_line = ttk.Style()
        cstm_line.configure('LabelLine.TFrame', background='#43e871')
        title_sep = ttk.Separator(self.root, orient='horizontal', style='LabelLine.TFrame')
        title_sep.pack(fill='x',pady=10)
    def get_empty_index(self):
        emptyFound = False
        for i in range(len(self.word_guess)):
            j = 0
            while(j < 5):
                if self.word_guess[i][j] == '':
                    emptyFound = True
                    break
                j += 1
            if emptyFound:
                break
        if(not emptyFound):
            j = -1 #Indicates that there is not an empty box available, meaning all rows are completed and awaiting enter on the last row
        return (i, j)
    def find_last_entry(self):
        last_entry_index = []
        empty_ind = self.get_empty_index()
        if(empty_ind[1] == -1):
            last_entry_index = [empty_ind[0],4]
        elif empty_ind[1] == 0:
            last_entry_index = [empty_ind[0] - 1, 4]
        else:
            last_entry_index = [empty_ind[0], empty_ind[1] - 1]
        return last_entry_index
    def display_letter(self,letter):
        __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))) #Getting current file directory
        image_path = os.path.join(__location__, 'Images', 'letter_'+letter+'.png')
        letter_image = Image.open(image_path)
        image_photo = ImageTk.PhotoImage(letter_image)
        self.image_list.append(image_photo)
        last_entry_index = self.find_last_entry()
        #We find the corresponding rectange to the current entry, get its coordinates, find its center, and place our image there
        pos_image = self.word_disp.coords(self.boxes[last_entry_index[0]][last_entry_index[1]])
        pos_image_x = (pos_image[2] + pos_image[0])/2
        pos_image_y = (pos_image[3] + pos_image[1])/2
        self.word_disp.create_image(pos_image_x,pos_image_y, image = image_photo)        
    def delete_last_entry(self):
        image_photo = self.image_list.pop(len(self.image_list) - 1)
        del image_photo     
        delete_ind = self.find_last_entry()
        self.word_guess[delete_ind[0]][delete_ind[1]] = ''   
    def update_boxes(self, index):
        if index >= 5:
            self.updating_row = FALSE
            if(self.get_empty_index()[1] == -1):
                self.guess_row = -1
            return
        box_id = self.boxes[self.guess_row - 1][index]
        color = ''
        if(self.sol_word[index] == self.word_guess[self.guess_row - 1][index]):
            color = '#43e871'
        elif(self.word_guess[self.guess_row - 1][index] in self.sol_word):
            color = '#e8cd43'
        else:
            color = '#454545'
        self.word_disp.itemconfigure(box_id, fill=color)
        self.word_disp.after(self.update_speed, self.update_boxes, index + 1) #BUGGY
        #self.update_boxes(index + 1)
    def onKeyPress(self, event):
        empty_ind = self.get_empty_index()
        if event.keysym == 'BackSpace': 
            if self.find_last_entry()[0] != self.guess_row:
                print("Cannot delete entry from previous entered word")
            else: 
                self.delete_last_entry()
                #print(self.word_guess)
        elif event.keysym == 'Return':
            if (empty_ind[1] >= 0 and empty_ind[0] != self.guess_row) or empty_ind[1] == -1: #Check if the row is completed, empty_ind = -1 if theres no more rows below and last 'box' is occupied
                if(self.guess_row == -1):
                    print("Round is finished")
                else:
                    self.guess_row += 1
                    self.updating_row = True
                    self.update_boxes(0)
            else:
                print("Row not completed")
            print("Enter")
        elif(self.updating_row):
            print("Row currently updating, wait")  
        elif event.char.isalpha():
            if empty_ind[0] != self.guess_row:
                print("Do nothing")
            elif self.word_guess[empty_ind[0]][empty_ind[1]] == '':
                #print("Valid entry")
                self.word_guess[empty_ind[0]][empty_ind[1]] = event.char.lower()
                self.display_letter(event.char)
                #print(self.word_guess)
            else:
                print('last row occupied, awaiting enter or backspace')
        # else:
        #     print("Not valid entry")
root = Tk()
root.geometry("900x1000")
start = Mordle(root)
root.mainloop()