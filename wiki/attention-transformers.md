# Attention and Transformers

The attention mechanism was invented to overcome the bottleneck in RNN-based sequence-to-sequence models. It has since become the dominant building block of modern AI, powering large language models, vision transformers, and multimodal systems.

## Source

- `raw/03-stanford-cs231n/Stanford CS231N.md`

## The Problem Attention Solves

In a classic RNN encoder-decoder (for translation):
- The encoder compresses the entire input sentence into one fixed-size vector
- The decoder generates output from that single vector
- **Bottleneck:** the fixed-size vector loses information for long sequences

**Analogy without attention:** read a paragraph, someone takes it away, then translate everything from memory.

**Analogy with attention:** read a paragraph, then look back at any specific word whenever you need it while translating.

## Attention Mechanism

Instead of one fixed context vector, attention computes a **new context vector at every decoder step** by taking a weighted sum of all encoder hidden states.

### How Attention Weights Are Computed

1. Compare decoder state `hₜ` against each encoder state `hᵢ` using a score function
2. Apply softmax to get attention weights `aₜᵢ` (soft probabilities that sum to 1)
3. Weighted sum: `cₜ = Σ aₜᵢ · hᵢ`

**Soft vs Hard Attention:**
- **Soft attention** (standard): weighted sum over all positions — differentiable, trainable via backprop
- **Hard attention**: select exactly one position (argmax) — not differentiable; requires special training

## The General Attention Layer

Attention as an **information retrieval system** (like a Google search):
- **Query (Q):** what you're looking for
- **Keys (K):** index labels for each stored item
- **Values (V):** the actual content stored at each position

```
Attention(Q, K, V) = softmax(QKᵀ / √d) · V
```

- `√d` scaling prevents softmax from saturating in high dimensions
- Self-attention: Q, K, V all come from the same sequence
- Cross-attention: Q comes from one sequence, K and V from another

## Self-Attention

A **self-attention layer** relates all positions in a single sequence to each other:
- Each token attends to every other token
- Captures global dependencies regardless of distance (unlike RNNs and CNNs)

**Problem:** self-attention has no notion of position — the order of tokens doesn't matter by default.

**Solution: Positional Encoding** — add position information to the input embeddings before attention.

## Masked Self-Attention

A variant where tokens cannot attend to **future positions**:
- Used in autoregressive language modeling (predicting the next token)
- The mask sets future positions to `-∞` before softmax, zeroing them out
- Prevents "cheating" — the model at position t cannot see positions t+1, t+2, ...

## Multi-Head Attention

Instead of one attention function, run H attention heads in parallel:

```
MultiHead(Q, K, V) = Concat(head₁, ..., headH) · Wₒ
headᵢ = Attention(Q·Wᵢᵠ, K·Wᵢᴷ, V·Wᵢᵛ)
```

- Each head learns to attend to different types of relationships
- Self-attention in practice is **always** multi-head attention today
- Self-attention = just four matrix multiplies (Q, K, V projections + output projection)

## Transformer Architecture

A transformer block = multi-head self-attention + feedforward network, with residual connections and layer normalization:

```
x = x + MultiHeadAttention(LayerNorm(x))   # residual + attention
x = x + FFN(LayerNorm(x))                  # residual + MLP
```

### Encoder-Decoder vs Decoder-Only

| Architecture | Uses | Examples |
|---|---|---|
| Encoder-decoder | Translation, summarization | T5, BART |
| Decoder-only | Language modeling, generation | GPT, LLaMA, Claude |
| Encoder-only | Classification, retrieval | BERT, RoBERTa |

## Vision Transformer (ViT)

ViT applies the transformer to images by treating image patches as tokens:
1. Split image into fixed-size patches (e.g., 16×16 pixels)
2. Flatten each patch → linear projection → embedding vector
3. Add positional encodings
4. Feed sequence of patch embeddings through standard transformer layers

**Key insight:** ViTs use self-attention instead of convolutions as the main computation.

- ViT can "see" the whole image at once (global context from the first layer)
- CNNs build up receptive fields gradually through layers
- ViTs outperform CNNs given enough data and compute

## Attention Complexity

Attention is **quadratic** in sequence length:
- For N tokens, computing QKᵀ requires N² operations
- Long sequences (documents, video) become expensive
- This is why modern RNN variants (linear attention, Mamba) are competitive for long contexts

## Related Topics

- [[recurrent-neural-networks]] — the predecessor; attention was invented to fix RNN limitations
- [[convolutional-neural-networks]] — CNNs vs ViT in vision; transformers replacing convolutions
- [[neural-networks]] — backpropagation, loss functions
- [[optimization]] — AdamW + warm-up scheduling standard for transformers
- [[computer-vision]] — ViT for image classification, dense prediction
- [[nlp]] — transformers dominate all NLP tasks
- [[multimodal-models]] — transformer-based multimodal architectures (CLIP, BLIP)
