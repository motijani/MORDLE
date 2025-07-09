# src/train.py
import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader, random_split
import matplotlib.pyplot as plt

from dataset import MordleHistoryDataset
from model_architecture import SolutionPredictor

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# --- prepare vocab & data ---
all_words = [
    w.strip()
    for w in open(r'C:/Users/MOMO/Documents/Python Projects/Wordle/MORDLE/Training_Data/solution_words.txt')
]
word2idx = {w: i for i, w in enumerate(all_words)}

full_dataset = MordleHistoryDataset(
    r'C:/Users/MOMO/Documents/Python Projects/Wordle/MORDLE/Algorithm_Output/wordle_data_v2-1.csv',
    word2idx,
    max_steps=6
)

train_size = int(0.8 * len(full_dataset))
val_size   = len(full_dataset) - train_size
train_ds, val_ds = random_split(full_dataset, [train_size, val_size])

train_loader = DataLoader(train_ds, batch_size=64, shuffle=True,  drop_last=True)
val_loader   = DataLoader(val_ds,   batch_size=64, shuffle=False, drop_last=False)

model   = SolutionPredictor(vocab_size=len(all_words)).to(device)
opt     = optim.Adam(model.parameters(), lr=3e-4)
loss_fn = nn.CrossEntropyLoss()

epochs = list(range(1, 30))
train_losses, val_losses = [], []
train_top1, train_top5   = [], []
val_top1, val_top5       = [], []

for epoch in epochs:
    model.train()
    tloss = t1 = t5 = tot = 0

    for guesses, fb, sol_id in train_loader:
        guesses, fb, sol_id = guesses.to(device), fb.to(device), sol_id.to(device)
        logits = model(guesses, fb)               # (B, V)
        loss   = loss_fn(logits, sol_id)

        opt.zero_grad()
        loss.backward()
        opt.step()

        B = sol_id.size(0)
        tloss += loss.item() * B
        preds1 = logits.argmax(dim=1)             # (B,)
        t1    += (preds1 == sol_id).sum().item()

        top5 = logits.topk(5, dim=1).indices      # (B,5)
        t5  += sum(sol_id[i].item() in top5[i] 
                   for i in range(B))
        tot += B

    train_losses.append(tloss/tot)
    train_top1.append(t1/tot)
    train_top5.append(t5/tot)

    # — Validation —
    model.eval()
    vloss = v1 = v5 = vtot = 0

    with torch.no_grad():
        for guesses, fb, sol_id in val_loader:
            guesses, fb, sol_id = guesses.to(device), fb.to(device), sol_id.to(device)
            logits = model(guesses, fb)
            loss   = loss_fn(logits, sol_id)

            B = sol_id.size(0)
            vloss += loss.item() * B
            preds1 = logits.argmax(dim=1)
            v1    += (preds1 == sol_id).sum().item()

            top5 = logits.topk(5, dim=1).indices
            v5   += sum(sol_id[i].item() in top5[i] 
                        for i in range(B))
            vtot += B

    val_losses.append(vloss/vtot)
    val_top1.append(v1/vtot)
    val_top5.append(v5/vtot)

    print(
        f"Epoch {epoch:2d}  "
        f"Train Loss={train_losses[-1]:.4f}  "
        f"T1={train_top1[-1]:.2%}  T5={train_top5[-1]:.2%}  |  "
        f"Val Loss={val_losses[-1]:.4f}  "
        f"T1={val_top1[-1]:.2%}  T5={val_top5[-1]:.2%}"
    )

plt.figure()
plt.plot(epochs, train_losses,    label='Train Loss')
plt.plot(epochs, val_losses,      label='Val Loss')
plt.xlabel('Epoch'); plt.ylabel('Loss')
plt.legend(); plt.title('Loss over Epochs')
plt.show()

plt.figure()
plt.plot(epochs, train_top1,  label='Train Top-1')
plt.plot(epochs, val_top1,    label='Val Top-1')
plt.plot(epochs, train_top5,  label='Train Top-5')
plt.plot(epochs, val_top5,    label='Val Top-5')
plt.xlabel('Epoch'); plt.ylabel('Accuracy')
plt.legend(); plt.title('Accuracy over Epochs')
plt.show()
