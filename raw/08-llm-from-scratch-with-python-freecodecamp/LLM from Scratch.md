
Notes from the freeCodeCamp course on building a large language model from scratch in Python.

---

## Table of Contents

- [nn.Linear — Linear Layer](#nnlinear--linear-layer)
- [softmax — Softmax Function](#softmax--softmax-function)
- [Gradient Descent — Optimizers](#gradient-descent--optimizers)
- [BigramLanguageModel](#bigramlanguagemodel)

---

## nn.Linear — Linear Layer

`nn.Linear(in, out)` applies a linear transformation: `output = input @ W^T + bias`

Weights are stored as shape `(out_features, in_features)` — each row is the weight vector
for one output neuron. To multiply a row-vector input `(1, in)` against those rows, PyTorch
transposes W before the multiplication.

```
Weight matrix W  (shape: out × in = 3 × 3)
Each row = weights for one output neuron

       in0   in1   in2
  W = | w00  w01  w02 |   ← neuron 0
      | w10  w11  w12 |   ← neuron 1
      | w20  w21  w22 |   ← neuron 2


Transpose W^T  (shape: in × out = 3 × 3)

        out0  out1  out2
W^T = | w00  w10  w20 |
      | w01  w11  w21 |
      | w02  w12  w22 |


Input x (row vector, shape 1 × 3)

x = | 10  10  10 |


Multiply:  x @ W^T  →  (1×3) @ (3×3) = (1×3)

| 10  10  10 | @ | w00  w10  w20 |  =  | out0  out1  out2 |
               | w01  w11  w21 |
               | w02  w12  w22 |

Each output = dot product of x with one row of W:

  out0 = 10·w00 + 10·w01 + 10·w02   ← dot(x, row 0 of W)
  out1 = 10·w10 + 10·w11 + 10·w12   ← dot(x, row 1 of W)
  out2 = 10·w20 + 10·w21 + 10·w22   ← dot(x, row 2 of W)
```

---

## softmax — Softmax Function

`softmax(x, dim)` converts raw scores (logits) into probabilities that sum to 1.

```
formula:  softmax(x_i) =        e^(x_i)
                          ─────────────────────────
                          e^(x_0) + e^(x_1) + ... + e^(x_n)
```

### Why e^x?

`e` (Euler's number ≈ 2.718) arises naturally from continuous compounding — when a quantity
grows at a rate proportional to its current size, e appears. It has one unique property:

```
d/dx (e^x) = e^x     ← the only function that is its own derivative
```

Softmax uses e^x for three reasons:

**1. Always positive** — logits can be any value; probabilities must be > 0

```
e^(-100) ≈ 0.000...   (tiny but never zero or negative)
e^(0)    = 1
e^(100)  ≈ huge
```

**2. Preserves order** — if score A > score B then e^A > e^B, ranking is never flipped

**3. Amplifies differences** — each +1 in logit multiplies output by e (compounding effect)

```
logits:      [  1,     2,     3   ]   gap between each = 1
after e^x:   [  2.72,  7.39,  20.1]   gap keeps multiplying by ~2.72
softmax:     [  0.09,  0.24,  0.67]   highest score dominates clearly
```

Compare with naive linear normalization — it breaks with negative inputs:

```
logits [-3, -2, -1] → sum = -6 → negative probabilities (invalid)
e^x    [0.05, 0.14, 0.37] → sum = 0.56 → divide safely → valid probabilities
```

### Step-by-step example

```
input:       t4 = [1., 2., 3.]

step 1 — apply e^x to each element:
  e^1 = 2.718
  e^2 = 7.389
  e^3 = 20.086
  sum = 30.193

step 2 — divide each by the sum:
  2.718  / 30.193 = 0.0900
  7.389  / 30.193 = 0.2447
  20.086 / 30.193 = 0.6652

output:  [0.0900, 0.2447, 0.6652]   ← sums to 1.0
```

## Gradient Descent — Optimizers

An **optimizer** is the algorithm that updates model weights after each backward pass to reduce the loss. Gradient descent is the foundation: move each weight in the direction that decreases the loss, scaled by a learning rate.

```
update rule:   w  ←  w  −  lr · ∂L/∂w

  w      = current weight
  lr     = learning rate — a scalar multiplier applied to the gradient
  ∂L/∂w  = gradient of the loss with respect to w
```

`lr` is literally multiplied against the gradient before the weight is updated. It controls how large each step is:

```
gradient = 0.5,  lr = 0.01  →  weight update = 0.005   (small step)
gradient = 0.5,  lr = 1.00  →  weight update = 0.500   (large step)
```

The gradient tells you the slope — which direction increases the loss. Subtracting it moves the weight downhill toward a lower loss.

### PyTorch Optimizer API

All optimizers in `torch.optim` share the same interface:

```python
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# inside the training loop:
optimizer.zero_grad()   # clear gradients from the previous step
loss.backward()         # compute new gradients via backprop
optimizer.step()        # update weights using those gradients
```

`zero_grad()` is required before each backward pass — PyTorch accumulates gradients by default, so without it each step adds on top of the last.

### Common PyTorch Optimizers

| Optimizer | `torch.optim` class | Key idea |
|---|---|---|
| SGD | `SGD` | Plain gradient descent; optionally adds momentum |
| SGD + Momentum | `SGD(momentum=0.9)` | Accumulates a velocity vector to dampen oscillations and speed up convergence |
| RMSprop | `RMSprop` | Divides each gradient by a running average of its recent magnitudes, adapting the lr per-parameter |
| Adam | `Adam` | Combines momentum (1st moment) and RMSprop (2nd moment); the default choice for most deep learning |
| AdamW | `AdamW` | Adam with decoupled weight decay; preferred for training transformers and LLMs |

### SGD vs Adam intuition

```
SGD — same step size for every parameter:
  large gradient → large step (can overshoot)
  small gradient → small step (can stall)

Adam — adaptive step size per parameter:
  large gradient → lr is scaled down automatically
  small gradient → lr is scaled up automatically
  result: more stable convergence across all weights
```

### Learning rate effect

```
lr too large  →  overshoots the minimum, loss diverges or oscillates
lr too small  →  converges correctly but very slowly
lr just right →  loss decreases smoothly each step
```

```
loss
 |
 |  *                    ← lr too large (diverges)
 |    *   *
 |      *   *    *
 |  * * * *             ← lr just right (converges)
 |          * * * *
 |                  *** ← lr too small (stalls)
 +─────────────────────▶ steps
```

### Weight Decay

**Weight decay** is a regularization technique that penalizes large weights, pushing the model to find simpler solutions and reducing overfitting.

It works by adding a small fraction of the weight's current value to the update, nudging every weight toward zero each step:

```
update rule with decay:   w  ←  w  −  lr · ∂L/∂w  −  lr · λ · w

  λ (lambda) = weight decay coefficient (e.g. 0.01)
  λ · w      = penalty proportional to the weight's current size
```

The `− lr · λ · w` term shrinks the weight slightly on every step regardless of the gradient. Weights that are not strongly supported by the data get pushed to zero; weights that matter resist the decay because their gradient keeps pulling them back.

```
no decay:      w can grow large if it keeps reducing loss
with decay:    w must justify its size every step — large weights are expensive
```

In PyTorch, weight decay is passed directly to the optimizer:

```python
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4, weight_decay=0.01)
```

`AdamW` is preferred over `Adam` for this because it applies weight decay directly to the weights (decoupled), whereas `Adam` incorrectly folds it into the gradient scaling and gets the math wrong.

---

## BigramLanguageModel

A bigram model predicts the next token based solely on the current token. It has a single learned parameter: an embedding table where each row is the score distribution over the vocabulary for what comes next.

```python
class BigramLanguageModel(nn.Module):
    def __init__(self, vocab_size: int) -> None:
        super().__init__()
        self.token_embedding_table = nn.Embedding(vocab_size, vocab_size)
```

### Embedding Table — Learned Parameters

> **Q: Do the scores in the embedding table come from somewhere, or are they learned?**

No. The table starts as random noise and is updated by the optimizer during training, exactly like any other weight matrix. The scores emerge from the data — the model gets penalized every time it assigns a low score to the token that actually came next, so over many steps the correct next-token scores rise.

```
epoch 0 (random, meaningless):
  a → [ 0.43, -0.12,  0.87, -0.55,  0.10]
  b → [-0.91,  0.34,  0.02,  0.78, -0.20]
  ...

epoch 1000 (learned from corpus):
  a → [-0.10,  2.31, -0.05, -0.08, -0.12]   ← 'b' score dominates → a is usually followed by b
  b → [-0.08, -0.11,  2.45, -0.09, -0.07]   ← 'c' score dominates → b is usually followed by c
  ...
```

### Logits Shape — (B, T, vocab_size)

> **Q: What does each dimension in the logits shape (B, T, vocab_size) represent?**

Note: `vocab_size` and `block_size` (sequence length T) are different numbers.

```
vocab:      { a:0, b:1, c:2, d:3, e:4 }   vocab_size = 5
block_size: 3                              T = 3  (sequence length)
batch_size: 2                              B = 2
```

For a batch of two sequences `"abc"` and `"bcd"`:

```
index shape: (B=2, T=3)
  [[0, 1, 2],    ← "abc"
   [1, 2, 3]]    ← "bcd"

logits shape after embedding lookup: (B=2, T=3, vocab_size=5)
```

Each position `(B, T)` holds a row of 5 scores — one per vocab token — answering:
*"given the token sitting at this position, how likely is each vocab token to follow?"*

```
B=0, T=0  token='a' → [0.1, 0.4, 0.2, 0.1, 0.2]  ← 'b' (index 1) is highest
B=0, T=1  token='b' → [0.1, 0.1, 0.5, 0.2, 0.1]  ← 'c' (index 2) is highest
B=0, T=2  token='c' → [0.1, 0.1, 0.1, 0.6, 0.1]  ← 'd' (index 3) is highest
B=1, T=0  token='b' → [0.1, 0.1, 0.5, 0.2, 0.1]  ← same row as B=0,T=1 — same token
B=1, T=1  token='c' → [0.1, 0.1, 0.1, 0.6, 0.1]
B=1, T=2  token='d' → [0.2, 0.1, 0.1, 0.1, 0.5]  ← 'e' (index 4) is highest
```

The bigram constraint: each position only looks at **its own token**. `T=1` has no idea what was at `T=0`.

### forward() vs generate()

> **Q: What is each method for, and why does generate() call forward() internally?**

They have opposite jobs:

```
forward()   → training   — takes input + targets, returns logits + loss
generate()  → inference  — takes a seed, extends it token by token, no loss
```

`forward` is the engine — it does the embedding lookup and loss computation. `generate` is a loop that drives `forward` repeatedly, grabs only the logits, and uses them to sample the next token.

```python
# training — both outputs used
logits, loss = model.forward(x, targets)
loss.backward()        # gradients flow back through logits → embedding table
optimizer.step()       # embedding table rows get nudged

# generation — loss is always None, discarded
logits, _ = model.forward(index)   # no targets passed
probs = F.softmax(logits[:, -1, :], dim=-1)
next_token = torch.multinomial(probs, num_samples=1)
```

> **Q: If forward() is used for training, why does it return the loss instead of updating the weights directly?**

The model doesn't update its own weights — that's the optimizer's job, and it lives outside the model. `forward` computes the loss and returns it so the training loop can call `loss.backward()` and `optimizer.step()`. The loss is a tensor (not a plain float) because `.backward()` needs the computation graph attached to it.

```python
# training loop (outside the model)
logits, loss = model(x, targets)
loss.backward()     # would fail if loss were a plain float
optimizer.step()
```

### torch.Tensor.view — Reshaping

> **Q: What does .view() do, and why is it needed here?**

`view` reshapes a tensor without changing its data — same numbers, different shape. The only rule is that the total element count must stay the same.

```python
# logits shape coming out of embedding: (B=2, T=3, C=5)  → 30 elements
logits = logits.view(B * T, C)   # → (6, 5)              → 30 elements

# F.cross_entropy needs (N, C) — flat list of predictions paired with targets
# view collapses the batch and sequence dimensions into one
```

```
-1 lets PyTorch infer the missing dimension:
  tensor of 12 elements:
  .view(3, -1)  → (3, 4)
  .view(-1)     → (12,)   flatten completely
```

### Training — Step by Step

> **Q: What does one full training step look like, from feeding the corpus to updating the weights?**

```
corpus:      "abcde abcde ..."
vocab:       { a:0, b:1, c:2, d:3, e:4 }   vocab_size = 5
block_size:  3                              (T=3, different from vocab_size)
batch_size:  1
```

**Epoch 0 — embedding table is random noise**

```
         a      b      c      d      e
  a → [ 0.3,  0.1,  0.6,  0.2,  0.1]
  b → [ 0.5,  0.4,  0.1,  0.3,  0.2]
  c → [ 0.2,  0.7,  0.1,  0.1,  0.3]
  d → [ 0.4,  0.1,  0.3,  0.2,  0.1]
  e → [ 0.1,  0.3,  0.2,  0.4,  0.2]
```

**Step 1 — get a batch**

```
x (input):   [[a, b, c]]  →  [[0, 1, 2]]   shape (1, 3)
y (targets): [[b, c, d]]  →  [[1, 2, 3]]   shape (1, 3)   ← x shifted right by 1
```

**Step 2 — forward pass**

```
lookup x → logits shape (1, 3, 5)

  T=0 token 'a' → [0.3, 0.1, 0.6, 0.2, 0.1]   target: 'b' (index 1)
  T=1 token 'b' → [0.5, 0.4, 0.1, 0.3, 0.2]   target: 'c' (index 2)
  T=2 token 'c' → [0.2, 0.7, 0.1, 0.1, 0.3]   target: 'd' (index 3)

view(B*T, C) → logits (3, 5),  targets.view(B*T) → [1, 2, 3]

cross_entropy per position:
  'a' → target 'b':  softmax → [..., 0.18, ...]  loss = -log(0.18) = 1.71  ← 'b' score too low
  'b' → target 'c':  softmax → [..., 0.16, ...]  loss = -log(0.16) = 1.83  ← 'c' score too low
  'c' → target 'd':  softmax → [..., 0.14, ...]  loss = -log(0.14) = 1.97  ← 'd' score too low

average loss = 1.84
```

**Step 3 — backward + optimizer step**

```
loss.backward()
  → gradients computed for every score in the embedding table
  → rows 'a', 'b', 'c' get gradients pushing the correct next-token score up

optimizer.step()  (lr = 0.1)
  → row 'a': 'b' score nudged up, others nudged down
  → row 'b': 'c' score nudged up, others nudged down
  → row 'c': 'd' score nudged up, others nudged down
```

**After many epochs**

```
loss converges toward 0

final embedding table:
         a      b      c      d      e
  a → [-0.1,  2.4, -0.1, -0.1, -0.1]   ← 'b' dominates
  b → [-0.1, -0.1,  2.4, -0.1, -0.1]   ← 'c' dominates
  c → [-0.1, -0.1, -0.1,  2.4, -0.1]   ← 'd' dominates
  d → [-0.1, -0.1, -0.1, -0.1,  2.4]   ← 'e' dominates
  e → [ 2.4, -0.1, -0.1, -0.1, -0.1]   ← 'a' dominates (cycle wraps around)
```
