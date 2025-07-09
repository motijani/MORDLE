import random
import os
import csv
def mark_indexes(base_word, guess):
    result = []
    for i in range(len(base_word)):
        if guess[i] == base_word[i]:
            result.append(2)
        elif guess[i] in base_word:
            result.append(1)
        else:
            result.append(0)
    return result

def select_word_without_letters(word_list, letters, search_loc):
    for word in word_list:
        if all(letter not in word for letter in letters):
            return word.strip()
    return None
#This function will read the list of solutions and return all the letters that are not found
def letters_not_exist(solution_words):
    all_letters = set('abcdefghijklmnopqrstuvwxyz')
    unique_letters = set(''.join(solution_words))
    missing_letters = all_letters - unique_letters
    return missing_letters

def check_index_letter_sequence(word,proper_index,proper_letter):
    all_letters = set()
    for l in proper_index:
        all_letters.add(l[0])
    for l in proper_letter:
        all_letters.add(l[0])
    #print(word_list)
    #Check if each item in proper_index matches with word
    if not all_letters.issubset(word): #Checks to see if the word contains all the letters that we know for sure are in the word
        return False
    for l in proper_index:
        letter_val = l[0]
        letter_index = l[1]
        if word[letter_index] != letter_val:
            return False
    # Check proper_letter
    for l in proper_letter:
        letter_val = l[0]
        letter_index = l[1]
        if word[letter_index] == letter_val:
            return False
    return True

    
def select_new_word(possible_solutions,word_list,guesses):
    #We will go through each guess already made and create a new list of match_indexes
    proper_index = []
    proper_letter = []
    wrong_letter = set()
    new_word_list = []
    for guess in guesses:
        match_list = match_indexes(guess)
        for item in match_list[2]:
            wrong_letter.add(item)
        for item in match_list[1]:
            proper_letter.append(item)
        for item in match_list[0]:
            proper_index.append(item)
    non_letters = letters_not_exist(possible_solutions)
    wrong_letter = wrong_letter|non_letters
    #Eliminate all words that have the wrong letter  
    for word in word_list:
        if any(letter in word for letter in wrong_letter):
            continue
        if check_index_letter_sequence(word,proper_index,proper_letter):
            new_word_list.append(word) 
    #Pick a new word that doesnt have any of the void letters, and also doesnt have any of the letters that is already used, and the word doesnt have more than 2 letters of the same
    return random.choice(new_word_list).strip()

def match_indexes(guess):
    rightIndex = [] #Stores all Index that have the correct letter in the correct position
    rightLetter = [] #Stores all letters that are in the word but not in the right index
    wrongLetter = [] #Stores all letters that do not exist in the word
    word = guess[0]
    matched_index = guess[1]
    for i in range(5):
        if matched_index[i] == 2: #Correct Position
            if rightIndex:
                letters_in = rightIndex[0]
                if(word[i] in letters_in):
                    break
            rightIndex.append((word[i],i))
        elif(matched_index[i] == 1):
            if rightLetter:
                letters_in = [letter[0] for letter in rightLetter]
                if word[i] in letters_in:
                    break
            rightLetter.append((word[i], i))
        else:
            wrongLetter.append(word[i])
    return ((rightIndex,rightLetter,wrongLetter))
                
def find_possible_solutions(solution_list, guesses):
    matched_index = []
    possible_solutions = []
    for guess in guesses:
        matched_index.append(match_indexes(guess))
    for sol in solution_list:
        isWord = True
        # Make sure for each word the rightIndex letter matches, the rightLetter is in the word but not in that position,
        # and the wrong letter is not in the word
        for match_index in matched_index:
            right_index = match_index[0]
            right_letter = match_index[1]
            wrong_letter = match_index[2]
            for l in wrong_letter:
                letter = l
                if letter in sol:
                    isWord = False
                    break
            if not isWord:
                break
            for l in right_letter:
                letter_val = l[0]
                letter_index = l[1]
                if sol[letter_index] == letter_val:
                    isWord = False
                    break
            if not isWord:
                break
            for l in right_index:
                letter_val = l[0]
                letter_index = l[1]
                if sol[letter_index] != letter_val:
                    isWord = False
                    break
            if not isWord:
                break
        if isWord:
            possible_solutions.append(sol)
    return possible_solutions


__location__ = os.path.realpath(
os.path.join(os.getcwd(), 'MORDLE', 'Training_Data')) #Getting current file directory

starting_words_path = os.path.join(__location__,'starting.txt')
with open(starting_words_path,'r') as file:
    starting_words = file.readlines()

starting_words_path_top100 = os.path.join(__location__,'top_100.txt')
with open(starting_words_path_top100,'r') as file:
    starting_words_100 = file.readlines()
        
random_words_path = os.path.join(__location__,'shuffled_data.txt')
with open(random_words_path, 'r') as file:
    random_words = file.readlines()

solution_words_path = os.path.join(__location__,'solution_words.txt')
with open(solution_words_path,'r') as file:
    solution_words = file.readlines()
    
og_solution_words = solution_words

solve_time = []
file = open('wordle_data_v2-1.csv', 'w', newline='')
writer = csv.writer(file)
writer.writerow(['Solution','Row#','Guesses'])
total_iterations = 100000
progress_interval = 10000
for i in range(total_iterations):
    if (i + 1) % progress_interval == 0:
            percent_completed = ((i + 1) / total_iterations) * 100
            print("Progress: {0}% completed".format(percent_completed))
    solution_words = og_solution_words
    word_to_solve = random.choice(solution_words).strip()
    #print("Word to slove is " + word_to_solve)
    current_guess = random.choice(starting_words).strip() #pick a starting word at random
    previous_guesses = [] #Store List of all guesses, with corresponding index value 0 1 2 for each letter ex; [Apple,00001]
    iterations = 1
    while True:
        #print("Guessing... {0}".format(current_guess))
        if (current_guess == word_to_solve):
            #print("Solved in {0} rows".format(iterations))
            writeRow = ""
            for i, guess_ind in enumerate(previous_guesses):
                writeRow += ''.join(str(x) for x in guess_ind)
                if i < len(previous_guesses):
                    writeRow += "/"
            writeRow += (word_to_solve + '[2, 2, 2, 2, 2]')
            writer.writerow([word_to_solve,iterations, writeRow])
            solve_time.append(iterations)
            break
        marked_Index = mark_indexes(word_to_solve, current_guess)
        previous_guesses.append((current_guess,marked_Index))
        if all(index == 0 for index in marked_Index): #None of the indexes are yellow nor green
            current_guess = select_word_without_letters(starting_words_100, current_guess, "Top 100") #Select from top 100 words
            if current_guess is None: #If there is no unique from top 100, search from random words
                current_guess = select_word_without_letters(random_words, current_guess, "Random")
        solution_words = find_possible_solutions(solution_words, previous_guesses)
        current_guess = select_new_word(solution_words,random_words,previous_guesses)
        iterations += 1
file.close()      
total = sum(solve_time)
average = total / len(solve_time)
print("Average after {0} executions is {1}".format(len(solve_time),average)) 
