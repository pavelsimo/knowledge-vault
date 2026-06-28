# %% [markdown]
# # Bigram Language Model

# %% Imports & Config
import os
import torch
import torch.nn as nn
from torch.nn import functional as F

device = 'cuda' if torch.cuda.is_available() else 'cpu'
block_size = 8
batch_size = 4

# %% Load Data
with open('../../wiki/china-development-economics.md', 'r', encoding='utf-8') as f:
    text = f.read()

# %% Vocabulary
chars = sorted(set(text))
print(chars)
print(len(chars))

# %% Encoder / Decoder
string_to_int = {ch:i for i, ch in enumerate(chars)}
int_to_string = {i:ch for i, ch in enumerate(chars)}

encode = lambda s: [string_to_int[c] for c in s]
decode = lambda l: ''.join([int_to_string[i] for i in l])

print(encode("hello"))
print(decode(encode("hello")))

# %% Tokenize
data = torch.tensor(encode(text), dtype=torch.long)
print(data.shape, data.dtype)
print("Train Sample:", data[:100])

# %% Train / Val Split
n = int(0.8 * len(data))
train_data = data[:n]
val_data = data[n:]
print(train_data.shape, val_data.shape)

def get_batch(split):
    data = train_data if split == 'train' else val_data
    ix = torch.randint(len(data) - block_size, (batch_size,))
    #print("Random indices:", ix)
    x = torch.stack([data[i:i+block_size] for i in ix])
    y = torch.stack([data[i+1:i+block_size+1] for i in ix])
    x, y = x.to(device), y.to(device)
    return x, y

# %% Blocks & Targets
# block size - the length of the sequence we want to feed into the model
# batch size - the number of sequences we want to feed into the model at once
x, y = get_batch('train')
print("X:", x)
print("Y:", y)
x = train_data[:block_size]
y = train_data[1:block_size+1]
for t in range(block_size):
    context = x[:t+1]
    target = y[t]
    print(f"when input is {context} the target: {target}")

@torch.no_grad()  # disable gradient tracking to save memory and speed up evaluation
def estimate_loss():
    out = {}
    model.eval()  # switch to eval mode so dropout/batchnorm behave correctly
    for split in ['train', 'val']:
        losses = torch.zeros(100)
        for k in range(100):
            X, Y = get_batch(split)
            logits, loss = model(X, Y)
            losses[k] = loss.item()  # store scalar loss for this batch
        out[split] = losses.mean()  # average over 100 batches for a stable estimate
    model.train()  # restore training mode before returning
    return out


class BigramLanguageModel(nn.Module):
    def __init__(self, vocab_size: int) -> None:
        super().__init__()
        self.token_embedding_table = nn.Embedding(vocab_size, vocab_size)

    def forward(
        self,
        index: torch.Tensor,                   # (B, T)  int64
        targets: torch.Tensor | None = None,   # (B, T)  int64
    ) -> tuple[torch.Tensor, torch.Tensor | None]:
        # PURPOSE: used during training — computes logits and the loss so the
        # optimizer can update the weights via loss.backward() + optimizer.step().
        # Also called by generate(), which only uses the logits and discards the loss.
        #
        # index:  (B, T) — a batch of B sequences, each T tokens long
        # Each token index is looked up in the embedding table, which returns a
        # row of vocab_size scores (logits) — one score per possible next token.
        logits = self.token_embedding_table(index)  # → (B, T, vocab_size)

        if targets is not None:
            B, T, C = logits.shape  # B=batch, T=seq_len, C=vocab_size

            # F.cross_entropy expects 2D logits (N, C) and 1D targets (N,).
            # We collapse B and T into one dimension so every token position
            # across every sequence becomes an independent prediction.
            logits  = logits.view(B * T, C)  # (B, T, C) → (B*T, C)
            targets = targets.view(B * T)     # (B, T)    → (B*T,)

            # For each position, cross_entropy softmaxes the logits and computes
            # -log(prob of the correct target token). Loss is the average over
            # all B*T positions.
            loss = F.cross_entropy(logits, targets)
        else:
            # No targets means we are generating, not training — skip the loss.
            loss = None

        return logits, loss

    def generate(
        self,
        index: torch.Tensor,   # (B, T)  int64 — seed sequence(s)
        max_new_tokens: int,
    ) -> torch.Tensor:         # (B, T + max_new_tokens)  int64
        # PURPOSE: used during inference — extends a seed sequence one token at a
        # time by repeatedly calling forward() to get logits, then sampling the
        # next token from those logits. No targets, no loss, no weight updates.
        #
        # index: (B, T) — the token sequence(s) so far, used as the seed.
        # We extend it one token at a time, up to max_new_tokens.
        for _ in range(max_new_tokens):
            # Run the forward pass on the whole sequence.
            # Loss is None here because we pass no targets.
            logits, loss = self.forward(index)  # logits → (B, T, C)

            # Bigram only needs the last token's scores to predict the next token.
            # All earlier positions are ignored.
            logits = logits[:, -1, :]  # (B, T, C) → (B, C)

            # Convert raw scores into probabilities that sum to 1.
            probs = F.softmax(logits, dim=-1)  # (B, C)

            # Sample one token per sequence from the probability distribution.
            # Higher-probability tokens are more likely to be picked, but it's
            # not always the top one — this randomness is what makes each
            # generated sequence different.
            next_token = torch.multinomial(probs, num_samples=1)  # (B, 1)

            # Append the sampled token to the sequence and loop again.
            index = torch.cat((index, next_token), dim=1)  # (B, T+1)

        return index  # (B, T + max_new_tokens)

vocab_size = len(chars)
model = BigramLanguageModel(vocab_size).to(device)

context = torch.zeros((1, 1), dtype=torch.long, device=device)
generated_chars = decode(model.generate(context, max_new_tokens=500)[0].tolist())
print("Generated chars:", generated_chars)

learning_rate = 3e-4
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
epochs = 100000

for epoch in range(epochs):
    # Sample a random batch of input sequences (xb) and their targets (yb).
    # xb and yb are the same data shifted by one position — each target is
    # the token that should follow the corresponding input token.
    xb, yb = get_batch('train')

    # Run the forward pass: look up embeddings, compute logits, and calculate
    # the cross-entropy loss measuring how wrong the current predictions are.
    logits, loss = model.forward(xb, yb)

    # Clear gradients from the previous step before computing new ones.
    # set_to_none=True frees the memory instead of filling it with zeros,
    # which is slightly faster.
    optimizer.zero_grad(set_to_none=True)

    # Backpropagation: compute the gradient of the loss with respect to every
    # parameter in the model (the embedding table rows in this case).
    # Each gradient says "nudge this value up or down to reduce the loss."
    loss.backward()

    # Apply the gradients: update every parameter by a small step in the
    # direction that reduces the loss, scaled by the learning rate.
    optimizer.step()

    if epoch % 500 == 0:
        losses = estimate_loss()
        print(f"Epoch {epoch+1}/{epochs}  train: {losses['train']:.4f}  val: {losses['val']:.4f}")

print(loss.item())

context = torch.zeros((1, 1), dtype=torch.long, device=device)
generated_chars = decode(model.generate(context, max_new_tokens=500)[0].tolist())
print("Generated chars:", generated_chars)