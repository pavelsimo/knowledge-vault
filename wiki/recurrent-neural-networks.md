# Recurrent Neural Networks

Recurrent Neural Networks (RNNs) are neural networks designed for sequential data where the order of elements matters. Unlike standard feedforward networks, RNNs maintain an internal **hidden state** that acts as memory, allowing them to carry information across time steps.

## Source

- `raw/03-stanford-cs231n/Stanford CS231N.md`

## Vanilla RNN (Elman RNN)

The simplest RNN. At each time step t, it takes:
- `xₜ` — current input
- `hₜ₋₁` — previous hidden state (memory)

And computes:
```
hₜ = tanh(W · [hₜ₋₁, xₜ] + b)
yₜ = W_y · hₜ
```

The **hidden state** is the internal memory of the RNN — it summarizes everything the model has seen up to time t.

## Applications of RNNs

- Language modeling (predict next word)
- Machine translation (seq-to-seq)
- Sentiment analysis
- Time series prediction
- Music generation

## RNN Tradeoffs

**Advantages:**
- Unlimited context length (in theory)
- Compute scales linearly with sequence length

**Disadvantages:**
- Cannot be parallelized (must process sequentially)
- Vanilla RNNs struggle with long-range dependencies (vanishing gradients)

## Multilayer RNNs

Stack multiple RNN layers on top of each other (stacked RNNs):
- Each layer processes the hidden states from the layer below
- Learns progressively more abstract temporal patterns

## Vanishing Gradient Problem

When backpropagating through many time steps, the gradient is multiplied by the same weight matrix repeatedly:
- If weights are slightly < 1: gradients shrink exponentially → vanish
- If weights are slightly > 1: gradients grow exponentially → explode

Result: vanilla RNNs effectively only remember ~10–20 steps back.

## LSTM (Long Short-Term Memory)

LSTMs address the vanishing gradient problem with **gates** and a separate **cell state**:

The LSTM has two streams of information:
- `hₜ` — hidden state (short-term memory, passed between time steps)
- `cₜ` — cell state (long-term memory, modified by gates)

### The Four Gates

| Gate | Purpose |
|------|---------|
| **Forget gate** `fₜ` | What to erase from cell state |
| **Input gate** `iₜ` | What new information to write |
| **Cell gate** `g̃ₜ` | Candidate values to add |
| **Output gate** `oₜ` | What part of cell state to expose as output |

```
fₜ = σ(Wf · [hₜ₋₁, xₜ] + bf)
iₜ = σ(Wi · [hₜ₋₁, xₜ] + bi)
g̃ₜ = tanh(Wg · [hₜ₋₁, xₜ] + bg)
oₜ = σ(Wo · [hₜ₋₁, xₜ] + bo)
cₜ = fₜ ⊙ cₜ₋₁ + iₜ ⊙ g̃ₜ
hₜ = oₜ ⊙ tanh(cₜ)
```

The cell state behaves like a **highway** — gradients can flow back without being repeatedly multiplied, similar to ResNet skip connections.

### Does LSTM Solve Vanishing Gradients?

Not completely, but it makes long-range learning much easier:
- Gradients can flow back through the cell state pathway without attenuation
- LSTM doesn't guarantee no vanishing/exploding gradients, but provides a cleaner path

LSTMs saw enormous success in NLP before the transformer revolution (2017–2018).

## Modern RNNs

Recent architectures (Mamba, RWKV, xLSTM) revisit RNNs with improvements:
- **Unlimited context length** — major advantage over transformers (which are quadratic in sequence length)
- **Linear compute scaling** with sequence length vs transformers' quadratic scaling
- Actively competing with transformers for long-sequence tasks

## Historical Note

The attention mechanism (now used in transformers) was originally developed to overcome RNN limitations in machine translation — see [[attention-transformers]].

## Related Topics

- [[neural-networks]] — foundational concepts (backprop, loss functions)
- [[attention-transformers]] — attention mechanism born from RNN limitations; now dominant
- [[optimization]] — training RNNs (gradient clipping for exploding gradients)
- [[nlp]] — primary domain where RNNs were applied
