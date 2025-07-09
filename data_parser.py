import pandas as pd

def parse_guesses_indices(guesses_indices_str):
    if not isinstance(guesses_indices_str, str):
        return [], []
    guesses = []
    feedback = []
    for entry in guesses_indices_str.split('/'):
        guess, feedback_str = entry.split('[')
        feedback_vals = list(map(int, feedback_str.strip(']').split(', ')))
        guesses.append(guess.lower())  # Convert guesses to lowercase
        feedback.append(feedback_vals)
    return guesses, feedback

def load_and_parse_data(file_path):
    # Load the dataset
    wordle_data = pd.read_csv(file_path)

    # Apply the function to parse 'Guesses[Indices]'
    wordle_data[['Guesses', 'Feedback']] = wordle_data['Guesses'].apply(parse_guesses_indices).apply(pd.Series)

    # Convert solutions to lowercase
    wordle_data['Solution'] = wordle_data['Solution'].str.lower()
    return wordle_data
