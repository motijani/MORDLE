# src/dataset.py
import re
import pandas as pd
import torch
from torch.utils.data import Dataset

class MordleHistoryDataset(Dataset):
    def __init__(self, csv_path, word2idx, max_steps=6):
        self.max_steps = max_steps
        self.word2idx  = word2idx
        pad_letter = len(word2idx)       # for padding guesses
        pad_fb     = 3                   # feedback values are 0,1,2 - use 3 to pad

        df = pd.read_csv(csv_path)
        df = df.dropna(subset=['Solution', 'Guesses']) #Drop empty or aka useless rows, like first try guesses
        print(df.tail())
        self.examples = []

        for _, row in df.iterrows():
            sol = row['Solution']
            raw = row['Guesses'] or ""
            # parse each "word[0,1,2,2,0]" entry
            parts = raw.split('/')
            history = []
            for p in parts:
                m = re.match(r'([a-z]{5})\[(.*?)\]', p.strip())
                if not m:
                    continue
                guess_word = m.group(1)
                fb_list    = list(map(int, m.group(2).split(',')))
                # encode letters as indices
                g_idxs = [word2idx.get(c, pad_letter) for c in guess_word]
                history.append((g_idxs, fb_list))

            # pad or truncate to max_steps
            while len(history) < max_steps:
                history.append(([pad_letter]*5, [pad_fb]*5))
            history = history[:max_steps]

            # build tensors
            guesses = torch.tensor([g for g,_ in history], dtype=torch.long)    # (T,5)
            feedback= torch.tensor([f for _,f in history], dtype=torch.long)    # (T,5)
            sol_id  = torch.tensor(word2idx[sol], dtype=torch.long)

            self.examples.append((guesses, feedback, sol_id))

    def __len__(self): 
        return len(self.examples)

    def __getitem__(self, idx): 
        return self.examples[idx]
