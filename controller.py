import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import data_parser
from guess_encoder import GuessEncoder, flatten_features

class WordleController:
    def __init__(self, file_path):
        self.file_path = file_path
        self.model = None
        self.encoder = GuessEncoder()
        self.word_list = []
        self.max_guesses = 6
       # self._load_and_train_model()
    
    def _load_and_train_model(self):
        print('Training model')
        # Load and parse data
        wordle_data = data_parser.load_and_parse_data(self.file_path)
        
        # Encode guesses
        self.encoder.fit(wordle_data['Guesses'])
        wordle_data = self.encoder.encode_guesses(wordle_data)
        
        # Store unique solutions (words)
        self.word_list = wordle_data['Solution'].unique()
        
        # Create a map from words to indices
        self.word_to_index = {word: idx for idx, word in enumerate(self.word_list)}
        self.index_to_word = {idx: word for word, idx in self.word_to_index.items()}
        
        # Convert solutions to indices
        wordle_data['Solution_Index'] = wordle_data['Solution'].map(self.word_to_index)
        
        # Combine feedback into a single list for each game
        wordle_data['Combined_Feedback'] = wordle_data['Feedback'].apply(lambda x: x[:self.max_guesses] + [[-1]*5]*(self.max_guesses-len(x)))
        
        # Flatten the features into a single array for each game
        wordle_data['Features'] = wordle_data.apply(lambda row: flatten_features(row['Encoded_Guesses'], row['Combined_Feedback']), axis=1)
        
        # Convert to numpy arrays
        X = np.array(wordle_data['Features'].tolist())
        y = wordle_data['Solution_Index'].values
        
        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train the model with adjusted parameters
        self.model = RandomForestClassifier(n_estimators=100, max_depth=10, max_features='sqrt')
        self.model.fit(X_train, y_train)
        print("Finished training")
    
    def predict_next_guess(self, past_guesses, past_feedback):
        # Encode the past guesses
        encoded_guesses = self.encoder.transform(past_guesses)
        
        # Combine feedback into a single list
        combined_feedback = past_feedback[:self.max_guesses] + [[-1]*5]*(self.max_guesses-len(past_feedback))
        
        # Flatten the features
        features = flatten_features(encoded_guesses, combined_feedback)
        
        # Convert to numpy array and reshape for prediction
        X_current = np.array(features).reshape(1, -1)
        
        # Predict the next word index
        predicted_word_index = self.model.predict(X_current)[0]
        
        # Convert the index back to the word
        predicted_word = self.index_to_word[predicted_word_index]
        
        return predicted_word

def flatten_features(encoded_guesses, combined_feedback):
    flat_features = []
    for guess, feedback in zip(encoded_guesses, combined_feedback):
        flat_features.extend(guess)
        flat_features.extend(feedback)
    return flat_features
