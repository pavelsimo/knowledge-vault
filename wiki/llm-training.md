# LLM Training

Building a production-quality large language model involves four sequential stages: pre-training a base model on massive unlabeled corpora, supervised fine-tuning (SFT) to instill instruction-following behavior, reward modeling to capture human preferences, and reinforcement learning from human feedback (RLHF) with PPO to align the model's outputs with those preferences. Each stage builds directly on the previous one, transforming a next-token predictor into a safe, helpful assistant — the same recipe behind ChatGPT and similar models.

## Sources

- [LLMs from Scratch – Practical Engineering from Base Model to PPO RLHF](https://www.youtube.com/watch?v=p3sij8QzONQ) — freeCodeCamp.org (2025)
- [Developing an LLM: Building, Training, Finetuning](https://www.youtube.com/watch?v=kPGTx4wcm_w) — Sebastian Raschka (2024)
- [Create a Large Language Model from Scratch with Python](https://www.youtube.com/watch?v=UU1WVnMk4E8) — freeCodeCamp.org (2023)
- Build an LLM from Scratch (book): https://amzn.to/4fqvn0D
- Code repository: https://github.com/rasbt/LLMs-from-scratch

---

## The Four-Stage Pipeline

```
Raw text corpus
       ↓
  [Stage 1] Pre-training ─── Base model (next-token predictor)
       ↓
  [Stage 2] Supervised Fine-Tuning ─── Instruction-following model
       ↓
  [Stage 3] Reward Modeling ─── Reward model (human preference scorer)
       ↓
  [Stage 4] RLHF with PPO ─── Aligned assistant model
```

Stage 1 consumes the most compute (thousands of GPUs, months of training). Stages 2–4 are relatively cheap but critical for usability and safety.

---

## Stage 1: Pre-Training

### What the Model Learns

Pre-training is the **next-token prediction** task: given a sequence of tokens, predict the next one. Run over hundreds of billions or trillions of tokens from diverse text corpora (books, websites, code, Wikipedia), this simple objective forces the model to internalize world knowledge, grammar, reasoning patterns, and factual associations.

The result is a **base model** (also called a foundation model). It is a powerful next-token predictor but not yet an assistant — it will continue any text you give it, not answer questions helpfully.

### Data Preparation

- **Corpus size**: GPT-3 trained on ~500B tokens (books + Wikipedia + web crawl). Modern models use trillions of tokens.
- **Batching**: inputs are fixed-length windows slid across the text. Each row in a batch is a contiguous sequence; targets are the same sequence shifted one position right.
- **Tokenization**: raw text is not fed character-by-character. A **BPE (Byte Pair Encoding)** tokenizer (GPT-style) or **SentencePiece** (LLaMA-style) builds a vocabulary of ~50K–262K subword units. Unknown words are broken into sub-tokens — no OOV crashes, just longer sequences.

### Decoder-Only Transformer Architecture

LLMs use a **decoder-only** (causal) transformer:

1. **Token embedding** — each token ID → dense vector (vocab × d_model table)
2. **Positional encoding** — position information added to embeddings (sinusoidal in original transformer; **RoPE** in modern models — see [[attention-transformers]])
3. **N × decoder blocks** — each block:
   - Masked multi-head self-attention (causal mask prevents attending to future tokens)
   - Feed-forward network (two linear layers + nonlinearity)
   - Residual connections + layer normalization (pre-norm in modern models: **RMSNorm** instead of LayerNorm)
4. **Language model head** — final linear projection to vocab logits, then softmax

**Causal masking**: during training, the attention matrix is zeroed out above the diagonal so token `t` can only attend to tokens 1…t. This enables training on all positions simultaneously while preserving autoregressive semantics.

**Cross-entropy loss**: at each position, the loss is `-log P(correct next token)`. Averaged over the batch and optimized with AdamW.

### Modern Architecture Enhancements

| Component | Original (2017) | Modern practice |
|---|---|---|
| Normalization | Post-LayerNorm | Pre-RMSNorm |
| Positional encoding | Sinusoidal absolute | RoPE (relative, rotary) |
| Activation | ReLU | SwiGLU |
| Attention efficiency | Full MHA | GQA / MQA + KV cache |
| Long context | — | Sliding window attention |
| Scale efficiency | Dense FFN | MoE (optional) |

- **RoPE** — encodes position as rotation of Q/K vectors; generalizes to longer contexts than absolute encodings. See [[gemma-4]] for p-RoPE.
- **RMSNorm** — simpler and faster than LayerNorm; divides by RMS of activations only.
- **SwiGLU** — gated linear unit activation: `SwiGLU(x, W, V, b, c) = Swish(xW + b) ⊙ (xV + c)`. Better gradient flow than ReLU.
- **Sliding window attention** — tokens only attend to the last K positions; dramatically reduces long-sequence compute. Interleaved with full global attention in Gemma 4. See [[gemma-4]].
- **KV cache** — during inference, past K and V matrices are cached and reused. Without it, every new token would recompute K/V for the entire prefix. See [[attention-transformers]].

### Training Infrastructure

- **Mixed-precision training** — forward/backward in FP16 or BF16; master weights in FP32; reduces VRAM 2× vs. pure FP32.
- **Gradient accumulation** — simulate large batch sizes when memory is tight by accumulating gradients over N micro-batches before stepping.
- **Checkpointing** — save model state periodically; allows resuming after interruption and evaluating intermediate checkpoints.
- **MoE layers** — replace dense FFNs with many smaller expert FFNs; a learned router selects top-k experts per token. Total params >> active params. See [[ai-model-architectures]] for the MoE architecture.

---

## Stage 2: Supervised Fine-Tuning (SFT)

### From Predictor to Assistant

The base model completes text. SFT teaches it to **follow instructions** by training on curated examples of (instruction, response) pairs. The training objective is the same (next-token prediction) but the data distribution shifts from raw web text to structured human-written Q&A.

### Instruction Dataset Format

Each training example is formatted into a **chat template**, e.g.:

```
<|system|>You are a helpful assistant.<|end|>
<|user|>Explain gradient descent in one paragraph.<|end|>
<|assistant|>Gradient descent is an iterative optimization algorithm...<|end|>
```

Only the assistant response tokens contribute to the loss — the instruction prefix is used as context but not supervised.

### Types of Fine-Tuning

| Type | Data | Goal |
|---|---|---|
| **Classification fine-tuning** | labeled examples (text, label) | Spam detection, sentiment analysis |
| **Instruction fine-tuning** | (instruction, response) pairs | General assistant behavior |
| **Preference fine-tuning** | (prompt, chosen, rejected) triples | Align with human preferences (setup for RLHF) |

SFT is relatively compute-cheap. A strong base model + small high-quality instruction dataset can yield a capable assistant model in hours.

---

## Stage 3: Reward Modeling

### What a Reward Model Does

A reward model scores any (prompt, completion) pair with a scalar — higher is better from a human perspective. It is used in Stage 4 to provide a differentiable training signal for RLHF.

### Architecture

The reward model is typically initialized from the SFT model with an additional **value head**: a linear layer on top of the final transformer hidden state that outputs a single scalar reward.

### Training Data: Pairwise Preferences

Human annotators compare two model completions for the same prompt and pick the better one. This yields triples `(prompt, chosen, rejected)`.

**Bradley-Terry model**: models the probability that response A is preferred over B as:

```
P(A ≻ B) = σ(r(A) − r(B))
```

where r(·) is the reward model's output.

**Training objective** (margin ranking loss):

```
L = −log σ(r(chosen) − r(rejected))
```

The reward model is trained to assign higher scores to chosen completions than rejected ones.

---

## Stage 4: RLHF with PPO

### The Setup

| Component | Role |
|---|---|
| **Policy model** | The fine-tuned LLM being aligned; generates completions |
| **Reference model** | Frozen copy of the SFT model; provides the KL anchor |
| **Reward model** | Frozen; scores completions with a scalar |
| **Value model** | Predicts expected future reward; trained alongside policy |

### PPO Training Loop

For each step:

1. Sample a prompt from the dataset
2. **Policy model generates** a completion (stochastic decoding)
3. **Reward model scores** the completion → scalar reward `r`
4. **KL penalty** computed: `KL(policy || reference)` — measures how far the policy has drifted from the SFT baseline
5. **Adjusted reward**: `r_adjusted = r − β × KL`
6. **PPO update**: optimize the policy to maximize `r_adjusted` using clipped surrogate objective

### KL Penalty: Why It Matters

Without the KL penalty, the policy quickly learns to "game" the reward model — generating high-reward but incoherent or unsafe text (reward hacking). The KL term anchors the policy near the SFT model, ensuring it stays grammatically sensible and doesn't collapse to degenerate outputs.

**Intuition**: the reward model only captures what annotators prefer in the training distribution. The KL constraint prevents the policy from exploiting reward model blind spots.

### Proximal Policy Optimization (PPO)

PPO is a policy gradient method that prevents excessively large update steps via a **clipped surrogate objective**:

```
L_CLIP = E[min(r_t(θ) · A_t, clip(r_t(θ), 1−ε, 1+ε) · A_t)]
```

where:
- `r_t(θ)` = probability ratio (new policy / old policy)
- `A_t` = advantage estimate (how much better this action was than expected)
- `ε` = clip range (typically 0.1–0.2)

Clipping prevents the ratio from going too far from 1 in either direction, keeping updates stable. PPO is preferred over vanilla policy gradient (REINFORCE) for its stability and data efficiency.

---

## Autoregressive Inference

At inference time, a trained LLM generates text token by token:

1. Tokenize input prompt
2. Forward pass → logits for next token
3. Sample from logits (greedy, top-k, or nucleus sampling)
4. Append sampled token to context
5. Repeat until `<EOS>` token or max length

The KV cache stores past K/V matrices so each step only processes the new token, not the full prefix — O(N) per step instead of O(N²). See [[attention-transformers]] for KV cache mechanics.

---

## Practical Rules of Thumb

| Question | Guidance |
|---|---|
| How much pre-training data? | Hundreds of billions to trillions of tokens; more diverse data = better generalization |
| How much SFT data? | Quality >> quantity; thousands of high-quality examples often outperform millions of noisy ones |
| Fine-tune or prompt-engineer? | Fine-tune for consistent format/style changes; prompt-engineer for one-off tasks |
| Perplexity as eval? | Low perplexity ≠ good assistant; evaluate with downstream task accuracy or human preference |
| RLHF necessary? | RLHF dramatically improves safety and instruction-following; skip if building a base model only |

---

## Related Topics

- [[attention-transformers]] — transformer internals: QKV, causal masking, RoPE, KV cache
- [[neural-networks]] — loss functions, backpropagation, gradient computation
- [[optimization]] — AdamW, learning rate schedules, weight decay
- [[distributed-training]] — FSDP, ZeRO, tensor/pipeline parallelism for large-scale pre-training
- [[ai-model-architectures]] — MoE layers used in Stage 1 pre-training
- [[robot-learning]] — PPO and RL fundamentals also used in robotic policy learning
- [[gemma-4]] — concrete example of a modern pre-trained + fine-tuned multimodal LLM
