from controller import WordleController

class Process:
    def __init__(self):
        self.file_path = 'MORDLE\Algorithm_Output\wordle_data_v2-1.csv'  
        self.controller = WordleController(self.file_path)
        self.model = self.controller.model
    
    #Marks the index for classification 
    def mark_indexes(self, base_word, guess):
            result = []
            for i in range(len(base_word)):
                if guess[i] == base_word[i]:
                    result.append(2)
                elif guess[i] in base_word:
                    result.append(1)
                else:
                    result.append(0)
            return result
        
    def model_predict(self, sol_word, typed_word):
                guess = ''
                feedback = self.mark_indexes(sol_word,guess.join(typed_word))  #Gets the feedback based on the word guesses
                print(feedback)
                self.past_guesses.append(guess.join(typed_word))
                self.past_feedback.append(feedback)
                # next_guess = self.controller.predict_next_guess(self.past_guesses, self.past_feedback)
                next_guess = '00000'
                print("The model predicts you used the word ", next_guess)
    past_guesses = []
    past_feedback = []