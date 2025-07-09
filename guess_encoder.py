from sklearn.preprocessing import LabelEncoder
import string

class GuessEncoder:
    def __init__(self):
        self.le_guesses = LabelEncoder()

    def fit(self, guesses):
        # Create a list of all possible characters (a-z)
        all_chars = list(string.ascii_lowercase)
        self.le_guesses.fit(all_chars)

    def transform(self, guesses):
        # Encode and truncate guess count
        max_guesses = 5
        encoded_guesses = [self.le_guesses.transform(list(guess)) for guess in guesses]
        return encoded_guesses[:max_guesses] + [[-1]*5]*(max_guesses-len(encoded_guesses))

    def encode_guesses(self, wordle_data):
        wordle_data['Encoded_Guesses'] = wordle_data['Guesses'].apply(lambda x: self.transform(x))
        return wordle_data

def flatten_features(encoded_guesses, combined_feedback):
    flat_features = []
    for guess, feedback in zip(encoded_guesses, combined_feedback):
        flat_features.extend(guess)
        flat_features.extend(feedback)
    return flat_features
