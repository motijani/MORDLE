import time
import os
import random

def pick_word():
    wordList = []
    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))) #Getting current file directory
    with open(os.path.join(__location__, 'shuffled_data.txt')) as file:
      while line := (file.readline()).strip():
         wordList.append(line)
    randNum = random.randrange(len(wordList))
    return wordList[randNum]

def verify_input(word):
   return ((len(word) == 5) and word.isalpha()) #Makes sure word is 5 letters and it  contains only letters
    
print("This program is a terminal based wordle \n ...")
time.sleep(2)
word = pick_word()
guess_used = 0
curr_guess = ""
print("I've chosen a five letter word for you lets begin the guesses - {0}".format(word))
while(guess_used < 5):
    guess_used += 1
    curr_guess = input("Enter guess {0}\n".format(guess_used))
    if(curr_guess == word):
        print("You win")
        guess_used = 999 #Pending proper win function
        #design winning
    elif (not(verify_input(curr_guess))):
        print("That is not a Five-Letter Word silly, try again")
        guess_used -= 1
    else:
        for x in range(len(curr_guess)):
            if(curr_guess[x] == word[x]):
                print("Letter at pos {0} {1} is in the right position".format(x + 1,curr_guess[x]))
            elif(curr_guess[x] in word):
                print("Letter at pos {0} {1} is in the word".format(x + 1,curr_guess[x]))
        #Start the guessing process
