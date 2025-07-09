import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

import MORDLE.data_parser as data_parser
from MORDLE.guess_encoder import GuessEncoder, flatten_features

file_path = 'MORDLE\Algorithm_Output\wordle_data_v1-4.csv'
wordle_data = data_parser.load_and_parse_data(file_path)

#encode guesses
encoder = GuessEncoder()
encoder.fit(wordle_data['Guesses'])
wordle_data = encoder.encode_guesses(wordle_data)

#combine feedback into a single list for each game
max_guesses = 5
wordle_data['Combined_Feedback'] = wordle_data['Feedback'].apply(lambda x: x[:max_guesses] + [[-1]*5]*(max_guesses-len(x)))

#flatten to fit
wordle_data['Features'] = wordle_data.apply(lambda row: flatten_features(row['Encoded_Guesses'], row['Combined_Feedback']), axis=1)

#convert to np arrays
X = np.array(wordle_data['Features'].tolist())
y = encoder.le_guesses.transform(wordle_data['Solution'])


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#train the model on the data
model = RandomForestClassifier()
model.fit(X_train, y_train)

#predict based on the test
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Model Accuracy: {accuracy * 100:.2f}%")
