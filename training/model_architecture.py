# src/model.py
import torch.nn as nn
import torch

class SolutionPredictor(nn.Module):
    def __init__(self, vocab_size, max_steps=6, emb_dim=64, fb_dim=16, hid_dim=128):
        super().__init__()
        self.letter_emb = nn.Embedding(vocab_size+1, emb_dim, padding_idx=vocab_size)
        self.fb_emb     = nn.Embedding(4, fb_dim, padding_idx=3)
        in_dim = 5 * (emb_dim + fb_dim)

        self.lstm = nn.LSTM(in_dim, hid_dim, num_layers=2,
                            bidirectional=True, batch_first=True)
        self.classifier = nn.Linear(2*hid_dim, vocab_size)

    def forward(self, guesses, feedback):
        # guesses, feedback: (B, T, 5)
        g_e = self.letter_emb(guesses)    # (B, T, 5, emb_dim)
        f_e = self.fb_emb(feedback)       # (B, T, 5, fb_dim)
        x = torch.cat([g_e, f_e], dim=-1) # (B, T, 5, emb+fb)
        B, T, _, D = x.shape
        x = x.view(B, T, -1)              # flatten per‐guess: (B, T, 5*(emb+fb))
        out, _ = self.lstm(x)             # (B, T, 2*hid_dim)
        last = out[:, -1, :]              # (B, 2*hid_dim)
        return self.classifier(last)      # (B, vocab_size)
