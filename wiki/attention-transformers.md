# Attention and Transformers

The attention mechanism was invented to overcome the bottleneck in RNN-based sequence-to-sequence models. It has since become the dominant building block of modern AI, powering large language models, vision transformers, and multimodal systems.

## Source

- `raw/03-stanford-cs231n/Stanford CS231N.md`
- `raw/00-clippings/Math behind Attention - Q, K, and V.md`

## Three Ways of Processing Sequences

Before attention, there were two dominant approaches:

| Approach | Compute | Memory | Parallelizable? | Limitation |
|---|---|---|---|---|
| **RNN** | O(N) | O(N) | No | Must compute hidden states sequentially; no parallelism |
| **Convolution** | O(N) | O(N) | Yes | Must stack many layers to build up large receptive fields |
| **Self-Attention** | O(N²) | O(N) | Yes | Output depends directly on all inputs (just 4 matmuls) |

Self-attention is highly parallel (it's just matrix multiplications), but expensive: O(N²) compute for a sequence of length N. This is why attention in LLMs becomes a bottleneck for very long contexts.

(Vaswani et al., "Attention Is All You Need", NeurIPS 2017)

## The Problem Attention Solves

In a classic RNN encoder-decoder (for translation):
- The encoder compresses the entire input sentence into one fixed-size vector c (often c = h_T, the final hidden state)
- The decoder generates output from that single vector: decoder state s_t = g_U(y_{t-1}, s_{t-1}, c)
- **Bottleneck:** the fixed vector c must compress everything — "What if T=1000?"

Encoder: h_t = f_W(x_t, h_{t-1}) for "we see the sky" (x₁, x₂, x₃, x₄) → h₁, h₂, h₃, h₄ → c

Decoder: s₀ from c → predict y₁ "vediamo" → s₁ → y₂ "il" → s₂ → y₃ "cielo" → s₃ → y₄ [STOP]

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

**Self-Attention Layer — Full Computation:**

Inputs: input vectors X (N × D_in)
- Query matrix W_Q: D_in × D_out
- Key matrix W_K: D_in × D_out
- Value matrix W_V: D_in × D_out

1. K = X · W_Q → [N × D_out]
2. K = X · W_K → [N × D_out]
3. V = X · W_V → [N × D_out]
4. Similarities A = Q · Kᵀ / √(D_out) → [N × N]  (scaled dot-product)
5. E = softmax(A, dim=1) → [N × N]  (attention weights)
6. Output Y = E · V → [N × D_out]  (weighted sum of values)

**Problem:** self-attention has no notion of position — the order of tokens doesn't matter by default. The sequence [A, B, C] and [C, B, A] produce identical outputs.

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

A transformer block (Vaswani et al., "Attention Is All You Need", NeurIPS 2017):

```
Input: set of vectors x₁, x₂, x₃, x₄
  ↓
Self-Attention  ← all vectors interact through (multiheaded) self-attention
  ↓
  ⊕ residual connection
  ↓
Layer Normalization  ← normalizes all vectors
  ↓
MLP (per vector)  ← applied independently on each vector; classic setup is D → 4D → D
  ↓
Output: set of vectors y₁, y₂, y₃, y₄
```

Equivalently:
```
x = x + MultiHeadAttention(LayerNorm(x))   # residual + attention
x = x + FFN(LayerNorm(x))                  # residual + MLP
```

The MLP is sometimes called FFN (Feed-Forward Network). It applies the same 2-layer network independently to each position's vector — no interaction across positions at this stage.

### Modern Transformer Tweaks

The architecture has not changed much since 2017, but a few changes are now standard:

| Change | Original | Modern |
|---|---|---|
| **Pre-Norm** | LayerNorm after residual | LayerNorm before each sublayer (inside residual) |
| **RMSNorm** | LayerNorm | RMSNorm — simpler, no mean subtraction |
| **SwiGLU** | ReLU MLP | SwiGLU MLP — gated architecture |
| **MoE** | Dense MLP | Mixture of Experts: E different MLPs, activate A < E per token — massively more params, modest compute increase |

These tweaks are used in LLaMA, Mistral, Gemma, and most modern LLMs. The visual block now looks like: input → RMSNorm → Self-Attention → ⊕ → RMSNorm → MLP → ⊕ → output.

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

## Numeric Walkthrough: Scaled Dot-Product Attention

A step-by-step example with the sentence **"I love AI"** using tiny vectors (d_emb=4, d_k=3).

### Step 1 — Input embeddings (X, shape 3×4)

```
X = | 1  0  1  0 |   ← "I"
    | 0  1  0  1 |   ← "love"
    | 1  1  0  0 |   ← "AI"
```

### Step 2 — Project to Q, K, V using learned weight matrices

Q = X × W_Q,  K = X × W_K,  V = X × W_V

```
Q = | 2  0  1 |    K = | 0  1  1 |    V = | 1  0  1 |
    | 0  2  1 |        | 2  1  1 |        | 1  2  0 |
    | 1  1  1 |        | 1  1  1 |        | 1  1  0 |
```

### Step 3 — Attention scores: Q × Kᵀ

```
Scores = | 1  5  3 |   ← "I"
         | 3  3  3 |   ← "love"
         | 2  4  3 |   ← "AI"
```

"I" scores highest (5) toward "love".

### Step 4 — Scale by √d_k = √3 ≈ 1.732

Prevents softmax from saturating when dot products are large.

```
Scaled = | 0.577  2.887  1.732 |
         | 1.732  1.732  1.732 |
         | 1.155  2.309  1.732 |
```

### Step 5 — Softmax per row → attention weights

```
Weights = | 0.070  0.707  0.223 |   ← "I"
          | 0.333  0.333  0.333 |   ← "love"
          | 0.168  0.533  0.299 |   ← "AI"
```

"I" pays 70.7% attention to "love". "love" is neutral (equal 33.3% to all). Each row sums to 1.

### Step 6 — Weighted sum of values: Weights × V

```
Output = | 1.000  1.637  0.070 |   ← "I" (heavily influenced by "love"'s value)
         | 1.000  1.000  0.333 |   ← "love"
         | 1.000  1.365  0.168 |   ← "AI"
```

Each word's output is now a **context-aware blend** of all value vectors. This is how the model understands relationships between words.

## Attention Complexity

Attention is **quadratic** in sequence length:
- For N tokens, computing QKᵀ requires N² operations
- Long sequences (documents, video) become expensive
- This is why modern RNN variants (linear attention, Mamba) are competitive for long contexts

## KV Caching

KV caching eliminates redundant computation during autoregressive generation. It is why the first token from an LLM takes noticeably longer than subsequent tokens.

### The Redundancy Problem

During generation, each new token needs the hidden state of only the **most recent** token. But to compute that hidden state, every attention layer requires:
- The query (Q) vector of the latest token
- The key (K) and value (V) vectors of **every** previous token

This creates a compounding redundancy. Generating token 50 computes K and V for tokens 1–50. Generating token 51 recomputes K and V for tokens 1–50 again, from scratch, plus new ones for token 51. Tokens 1–49 were already computed and haven't changed — same inputs always produce the same outputs — yet the model discards and recomputes them every single step. That is O(n) redundant work per step, totaling O(n²) wasted compute over a full generation.

### The Fix

Instead of recomputing all K and V vectors at every step, store them. For each new token:

1. Compute Q, K, and V for only the newest token
2. Append the new K and V to the cache
3. Retrieve all previous K and V vectors from the cache
4. Run attention using the new Q against the full cached K and V

The expensive weight-matrix projections that produce K and V now happen exactly once per token in the sequence, not once per generation step. Attention still scales with sequence length (you attend over all cached keys and values), but the projection cost is eliminated. In practice this delivers roughly 5× speedup.

### Prefill Phase and Time-to-First-Token (TTFT)

There are two distinct phases in LLM inference:

**Prefill phase:** when you send a prompt, the model processes the entire input in one forward pass, computing and caching K and V vectors for every prompt token simultaneously. This is the most compute-intensive part of the request — and it is why the first token is slow. Longer prompts mean longer prefills, which mean longer waits.

**Generation phase:** once the cache is warm, each subsequent token needs only a single forward pass over one new token. The cache provides all previous context instantly from memory. This is why tokens stream out quickly after the first one.

The initial delay is called **time-to-first-token (TTFT)**. Optimizing TTFT — through chunked prefill, speculative decoding, or prompt caching — is an active area of LLM serving research.

### Memory Tradeoff

KV caching trades compute for GPU memory. Every transformer layer stores K and V vectors for every token in the sequence. For a large model like Qwen 2.5 72B (80 layers, 32K context, hidden dim 8192), the KV cache for a single request can consume several gigabytes of GPU memory. At hundreds of concurrent requests, the KV cache often exceeds the model weights themselves in total memory consumption.

This is why doubling context length is expensive: double the window means double the KV cache per request, which means fewer concurrent users on the same hardware.

**Solutions:**
- **Grouped-query attention (GQA)** — share key/value heads across multiple query heads; cuts KV cache size with minimal quality loss
- **Multi-query attention (MQA)** — extreme version: one K/V head shared across all query heads
- **Paged attention** — manages KV cache memory in non-contiguous pages (like OS virtual memory), enabling efficient sharing and reducing fragmentation; the core innovation in vLLM

Every major LLM serving stack — vLLM, TGI, TensorRT-LLM — is built on KV caching.

## Related Topics

- [[recurrent-neural-networks]] — the predecessor; attention was invented to fix RNN limitations
- [[convolutional-neural-networks]] — CNNs vs ViT in vision; transformers replacing convolutions
- [[neural-networks]] — backpropagation, loss functions
- [[optimization]] — AdamW + warm-up scheduling standard for transformers
- [[computer-vision]] — ViT for image classification, dense prediction
- [[nlp]] — transformers dominate all NLP tasks
- [[multimodal-models]] — transformer-based multimodal architectures (CLIP, BLIP)
- [[gpu-cuda]] — KV cache memory footprint and GPU VRAM constraints
- [[quantization]] — quantizing KV cache to reduce memory pressure
