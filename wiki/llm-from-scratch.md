LLM from Scratch is the hands-on path from PyTorch tensor mechanics to a tiny character-level language model. It complements the broader [[llm-training]] article by focusing on implementation fundamentals: tokenization, embedding tables, logits, cross-entropy, optimizer steps, causal masks, evaluation mode, and autoregressive generation.

## Sources

- [[raw/08-llm-from-scratch-with-python-freecodecamp/LLM from Scratch.md|raw/08-llm-from-scratch-with-python-freecodecamp/LLM from Scratch.md]]
- [[raw/08-llm-from-scratch-with-python-freecodecamp/bigram.py|raw/08-llm-from-scratch-with-python-freecodecamp/bigram.py]]
- [[raw/08-llm-from-scratch-with-python-freecodecamp/torch-examples.py|raw/08-llm-from-scratch-with-python-freecodecamp/torch-examples.py]]
- [[raw/08-llm-from-scratch-with-python-freecodecamp/requirements.txt|raw/08-llm-from-scratch-with-python-freecodecamp/requirements.txt]]

## PyTorch Building Blocks

The raw course notes start with the mechanics that make neural networks concrete:

| Concept | Practical meaning |
|---|---|
| `nn.Linear(in, out)` | Applies `output = input @ W.T + bias`; PyTorch stores weights as `(out_features, in_features)` |
| Softmax | Converts logits into positive probabilities that sum to 1 |
| Optimizer | Applies parameter updates after `loss.backward()` computes gradients |
| `zero_grad()` | Clears accumulated gradients before the next backward pass |
| `view()` | Reshapes tensors without changing the underlying values |
| `torch.tril()` mask | Builds the lower-triangular causal mask used by autoregressive attention |

The key mental model: tensors carry both values and, during training, a computation graph. The loss returned by `forward()` is still a tensor because `.backward()` needs that graph to compute gradients.

## Character Tokenization

The sample bigram model tokenizes text at the character level:

```python
chars = sorted(set(text))
string_to_int = {ch: i for i, ch in enumerate(chars)}
int_to_string = {i: ch for i, ch in enumerate(chars)}

encode = lambda s: [string_to_int[c] for c in s]
decode = lambda ids: "".join([int_to_string[i] for i in ids])
```

This is intentionally simple. Production LLMs use BPE, SentencePiece, or tokenizer variants described in [[nlp]], but character tokenization makes the mechanics visible.

## Bigram Model

A bigram language model predicts the next token from only the current token. It has one learned table:

```python
class BigramLanguageModel(nn.Module):
    def __init__(self, vocab_size: int) -> None:
        super().__init__()
        self.token_embedding_table = nn.Embedding(vocab_size, vocab_size)
```

Each row begins as random noise. Training changes the row so the score for the observed next token increases and competing scores decrease. For token `a`, the row eventually becomes a learned distribution over what tends to follow `a`.

The output shape is:

```text
logits: (B, T, vocab_size)
```

Where:

- `B` is batch size.
- `T` is sequence length, also called `block_size` in the raw code.
- `vocab_size` is the number of possible tokens.

Cross-entropy expects `(N, C)` logits and `(N,)` targets, so the model flattens batch and time:

```python
B, T, C = logits.shape
logits = logits.view(B * T, C)
targets = targets.view(B * T)
loss = F.cross_entropy(logits, targets)
```

## Training Loop

One training step looks like this:

```python
xb, yb = get_batch("train")
logits, loss = model(xb, yb)
optimizer.zero_grad(set_to_none=True)
loss.backward()
optimizer.step()
```

The target batch is the input shifted one token right. If `x = [a, b, c]`, then `y = [b, c, d]`. The loss asks: at each position, how much probability did the model assign to the actual next token?

Evaluation should run without gradients:

```python
@torch.no_grad()
def estimate_loss():
    model.eval()
    ...
    model.train()
```

`model.eval()` matters for models with dropout or batch norm, even though the tiny bigram model does not use those layers.

## Generation

Generation uses `forward()` without targets, samples the last-position logits, and appends one token at a time:

```python
logits, _ = model(index)
logits = logits[:, -1, :]
probs = F.softmax(logits, dim=-1)
next_token = torch.multinomial(probs, num_samples=1)
index = torch.cat((index, next_token), dim=1)
```

This is autoregressive inference in miniature. A modern decoder-only transformer does the same high-level loop, but with deep attention blocks, positional encodings, KV cache, larger vocabularies, and learned representations described in [[attention-transformers]].

## Related Topics

- [[llm-training]] - full pretraining, SFT, reward modeling, and RLHF pipeline
- [[attention-transformers]] - self-attention and decoder-only transformer mechanics
- [[neural-networks]] - loss functions, gradients, and backpropagation
- [[optimization]] - SGD, Adam, AdamW, and learning-rate behavior
- [[nlp]] - tokenization and language-processing tasks
