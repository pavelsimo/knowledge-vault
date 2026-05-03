# Gemma 4

Gemma 4 is Google DeepMind's fourth-generation family of open-weights multimodal language models, released in April 2026. The family spans four sizes — E2B, E4B (dense, on-device), 26B A4B (Mixture of Experts), and 31B (large dense) — all of which support image inputs with variable aspect ratios and resolutions. The two smallest models additionally support audio input via a Conformer-based encoder, making them capable of ASR and audio-language tasks. Key architectural innovations shared across the family include interleaved local/global attention with the final layer always global, a K=V trick to halve global-attention KV-cache size, p-RoPE to remove positional noise from low-frequency dimensions, and a ViT-based vision encoder with adaptive 2D-RoPE tiling. The E2B and E4B models further use Per-Layer Embeddings stored in flash memory to keep VRAM requirements tiny enough for on-device deployment.

## Sources

- [A Visual Guide to Gemma 4](https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-gemma-4) — Maarten Grootendorst (Google DeepMind), 2026-04-03
- [[raw/00-clippings/A Visual Guide to Gemma 4.md]]

## Model Variants

| Model | Type | Params (total) | Active params | Notable features |
|---|---|---|---|---|
| [Gemma 4 E2B](https://huggingface.co/google/gemma-4-e2b-it) | Dense | ~2B effective | All | Per-layer embeddings, audio encoder, 4:1 attention |
| [Gemma 4 E4B](https://huggingface.co/google/gemma-4-e4b-it) | Dense | ~4B effective | All | Per-layer embeddings, audio encoder, 5:1 attention |
| [Gemma 4 26B A4B](https://huggingface.co/google/gemma-4-26B-A4B-it) | MoE | 26B | 4B | 128 experts, 8 active + 1 shared, 5:1 attention |
| [Gemma 4 31B](https://huggingface.co/google/gemma-4-31b-it) | Dense | 31B | All | 60 layers, 5:1 attention, widest dense variant |

"E" = effective parameters (excludes flash-stored per-layer embeddings from VRAM count). "A" = active parameters during inference.

## Shared Architecture

All Gemma 4 variants are built around three pillars:

1. **Interleaved local + global attention** — efficient long-context processing
2. **Dense or MoE feedforward blocks** — capacity vs. compute tradeoff
3. **ViT-based vision encoder** — multimodal image understanding

![[raw/00-clippings/images/06ea6eebd56b14ccda834e69f3586644_MD5.webp]]

*The three pillars of Gemma 4: interleaved attention layers, either Dense or MoE feedforward blocks, and a vision encoder. Note: FFNNs are not interleaved — a variant uses exclusively Dense or exclusively MoE.*

---

## Interleaving Layers

Gemma 4 alternates **local attention** (sliding window) with **global attention** (full causal attention):

- **Local (sliding window)**: each token only attends to a limited window of prior tokens — 512 for E2B/E4B, 1024 for 26B/31B. Computationally cheap.
- **Global**: every token attends to the entire context. Expensive but essential for long-range coherence.

![[raw/00-clippings/images/0c98cc8cfd6118c001a3ef3ac4755aae_MD5.webp]]

*Sliding window attention: at each step only the last N tokens are in view, but hidden states carry information forward from earlier positions.*

![[raw/00-clippings/images/e4982f5300dc9e7471a3d79078b3f4b9_MD5.webp]]

*Example with a sliding window of 4: the visible window moves forward but previous hidden states still carry signal through the stack.*

**Interleaving pattern:**
- **E2B**: 4 local layers → 1 global layer (4:1 ratio)
- **All other variants**: 5 local layers → 1 global layer (5:1 ratio)
- **Critical change from Gemma 3**: the final layer is always a global attention layer in Gemma 4. In Gemma 3, the final layer was sometimes local, which limited long-range recall.

![[raw/00-clippings/images/948d80dca6e036aaad0782668a4c482d_MD5.webp]]

*Left: Gemma 3's 4:1 interleaving with a local final layer. Right: Gemma 4's pattern with the final layer always global.*

![[raw/00-clippings/images/0b2d1bcf742682ece5b4d2e84275c748_MD5.webp]]

*Side-by-side depth comparison of E2B (4:1) vs. larger variants (5:1), showing layer count and attention pattern differences.*

---

## Making Global Attention Efficient

Global attention attends to the full context on every token — expensive at long sequences. Gemma 4 applies three complementary tricks to reduce the cost.

### Grouped Query Attention (GQA)

Query heads share a smaller set of Key/Value heads, reducing KV-cache size:

- **Local layers**: 2 query heads share 1 KV head
- **Global layers**: 8 query heads share 1 KV head (larger grouping because global context is already much larger)
- To compensate for reduced KV expressiveness, the Key dimensionality is **doubled** in global layers.

![[raw/00-clippings/images/272602c16cc2b336638ad49d3ab94299_MD5.webp]]

*GQA in global attention: 8 queries per KV head. Key dimension is doubled to preserve representation quality.*

### K=V Trick

In the global attention layers, Keys are set equal to Values. This means only one matrix needs to be stored in the KV-cache instead of two — effectively converting a KV-cache into a K-cache for global layers.

![[raw/00-clippings/images/f920fcc873ab307835c4bcc3b444dded_MD5.webp]]

*K=V: the values matrix is discarded; the keys serve double duty as both keys and values in global attention.*

### p-RoPE

RoPE (Rotary Positional Encodings) encodes position by rotating Q/K pairs at decreasing frequencies. High-frequency pairs track word position; low-frequency pairs carry semantic meaning.

**The problem**: low-frequency pairs receive tiny positional rotations that add noise without meaningful position signal. Over long contexts, these small rotations accumulate and misalign distant tokens.

**The solution — p-RoPE**: apply RoPE to only the first `p` fraction of dimension pairs (p = 0.25 in Gemma 4), leaving the remaining 75% of pairs position-free and semantics-preserving.

![[raw/00-clippings/images/8f537ac33aadefa9fb6979f140f0677d_MD5.webp]]

*Standard RoPE: every pair gets a rotation. Low-frequency pairs (rightmost) receive almost no rotation, making the positional signal meaningless but adding noise.*

![[raw/00-clippings/images/1e812641fea8168e471e0a41508f635e_MD5.webp]]

*p-RoPE (p=0.25): only the first 25% of pairs receive positional rotations. The remaining 75% are left untouched for clean semantic representation.*

p-RoPE is applied only to **global** attention layers because that is where long contexts create the most problematic low-frequency accumulation.

### Summary: Global Attention Layer

Combined, the global attention layer in Gemma 4 applies:

1. Final layer is always global
2. 8 queries per KV head (GQA)
3. Key dimensionality doubled
4. Keys = Values (K=V)
5. p-RoPE with p = 0.25

![[raw/00-clippings/images/8565df156f34c5c5479d309af55d211a_MD5.webp]]

*Complete global attention layer: GQA with doubled key dim, K=V cache reduction, p-RoPE on the first 25% of dimensions.*

---

## Gemma 4 31B — Dense

The 31B model is the "vanilla" dense Gemma 4 variant — the cleanest representation of the base architecture without MoE or per-layer embeddings. It has 60 transformer layers (vs. 62 in Gemma 3 27B) but is wider, and uses the 5:1 interleaving pattern.

![[raw/00-clippings/images/83e167269569ad3e00ca4ebf74da4c9b_MD5.webp]]

*Gemma 4 31B architecture: 60 layers with 5:1 local/global interleaving and full global attention improvements.*

---

## Gemma 4 26B A4B — Mixture of Experts

The 26B A4B model replaces the dense FFNN in each layer with a **Mixture of Experts (MoE)** block:

- **128 total experts** — small FFNNs; only a subset activate per token
- **8 selected experts** per token — chosen by a learned router
- **1 shared expert** — always activated; 3× the size of a regular expert; encodes general world knowledge

![[raw/00-clippings/images/567729490ac74280b5ca25082a6658c7_MD5.webp]]

*MoE routing: for each token, a router assigns probabilities over all experts. The top-k experts are activated and their outputs are combined weighted by probability.*

![[raw/00-clippings/images/462515840837962b8b2d2b381a63a8b4_MD5.webp]]

*Shared expert (always on, 3× size) alongside 8 dynamically selected experts from a pool of 128.*

### Sparse vs. Active Parameters

- **Sparse (total) parameters**: all 26B — must be loaded into VRAM simultaneously
- **Active parameters**: only ~4B — the weights that actually compute during inference

Although the model occupies VRAM like a 26B model, it runs at approximately the speed of a 4B model.

![[raw/00-clippings/images/cdf73d5b22b0735c03ef67d5e321b76a_MD5.webp]]

*All 26B sparse parameters reside in VRAM; only 4B active parameters participate in each forward pass. The "A" in "26B A4B" refers to active parameters.*

> Note: MoE models require all expert weights in VRAM even though only a few fire per token. See [[gpu-cuda]] for the MoE VRAM trap.

---

## Gemma 4 E2B & E4B — Per-Layer Embeddings

The E2B and E4B models achieve on-device efficiency through **Per-Layer Embeddings (PLE)**:

### The "E" for Effective Parameters

Normally, a token embedding lookup table holds one embedding per vocabulary entry (262,144 tokens × 1,536 dims for E2B). PLE adds an additional, smaller embedding table **per layer** — a lookup that provides each token with layer-specific context cues.

| | E2B | E4B |
|---|---|---|
| Base embedding dim | 1,536 | 2,560 |
| PLE embedding dim | 256 | 256 |
| Layers | 35 | — |
| PLE table size | 262,144 × 35 × 256 | 262,144 × N × 256 |
| PLE storage | Flash memory | Flash memory |

![[raw/00-clippings/images/8c89ead9d30b7f3d2409eb5e39eacc27_MD5.webp]]

*Standard embedding layer: one embedding per token, loaded into VRAM.*

![[raw/00-clippings/images/58608d6871a9ded97d0eb87673da7d82_MD5.webp]]

*Per-Layer Embeddings: an additional, smaller lookup table per layer is stored in flash. At inference start, all needed embeddings are fetched once and cached.*

### How PLE Works

At inference start, the model fetches embeddings for all input tokens across all layers in one shot. Between each pair of decoder blocks:

1. The layer-specific PLE embedding is retrieved (dim: 256)
2. A **gating function** reweights each dimension
3. The result is **projected up** to the base embedding size (1,536 for E2B)
4. After RMSNorm, this is **added** to the decoder block's output

![[raw/00-clippings/images/d9a52548dcf62ad6217cd9626ada2437_MD5.webp]]

*PLE injection between decoder blocks: gating → projection → RMSNorm → residual add. The model is "reminded" of token identity at every layer.*

**Why it helps**: the model's internal dimensions can focus on contextual computation rather than carrying raw token identity through many layers. The PLE handles that bookkeeping from flash storage — off the critical VRAM path.

The "E" in E2B/E4B counts only parameters loaded into VRAM (the decoder weights), not the large PLE flash tables, making these models extremely VRAM-efficient for their capability level.

---

## Vision Encoder

All Gemma 4 variants process images through a **ViT-based vision encoder**.

### Standard ViT Recap

A Vision Transformer splits images into 16×16-pixel patches, treats them as tokens, and runs a transformer over the sequence. The output is one embedding per patch. See [[attention-transformers]] for the ViT paper.

![[raw/00-clippings/images/c414e76df667e5d9418415cda7dfa29e_MD5.webp]]

*ViT patch tokenization: image → 16×16 patches → transformer → one embedding per patch.*

### Variable Aspect Ratio via 2D RoPE

Standard ViT assumes square images. Non-square images assigned to a 1D patch sequence lose spatial meaning — patch #4 means different things in a 2×4 vs. 3×3 grid.

Gemma 4 replaces 1D RoPE with **2D RoPE**:
- Each patch embedding is split into two halves
- One half encodes horizontal position (width RoPE)
- The other half encodes vertical position (height RoPE)
- Images are adaptively padded (not distorted) to fit 16×16 patch boundaries

![[raw/00-clippings/images/a162908a2b6bc350a8ccbbba33010b37_MD5.webp]]

*2D RoPE: half the patch embedding dimensions encode width position, half encode height. This preserves spatial meaning regardless of aspect ratio.*

### Variable Resolution via Soft Token Budget

Gemma 4 supports 5 token budgets controlling how much the image is downscaled:

| Budget | Approximate resolution |
|---|---|
| 70 tokens | Very low (~small thumbnail) |
| 140 tokens | Low |
| 280 tokens | Medium |
| 560 tokens | High |
| 1120 tokens | Very high |

![[raw/00-clippings/images/4d8f372e2768ec643d0e52ac3e6c94a8_MD5.webp]]

*Token budget vs. effective resolution: higher budgets preserve finer detail at the cost of more tokens for the LLM to process.*

For a budget of N, the maximum patch count is `9 × N` (because every 3×3 block of neighboring patches is pooled into a single soft token by averaging).

![[raw/00-clippings/images/54437d8bc9844ba65b6fb9af5997427a_MD5.webp]]

*Spatial pooling: 3×3 blocks of patch embeddings are averaged into single soft tokens, compressing the visual representation to the budget size.*

### Linear Projection

Patch embeddings from the ViT have a different dimensionality than Gemma 4's token embeddings. A small learned linear network projects them into the LLM's embedding space, followed by RMSNorm.

- E2B/E4B: vision encoder has **150M parameters**
- 26B A4B, 31B: vision encoder has **550M parameters**

---

## Audio Encoder (E2B & E4B only)

The small models also accept audio input through a **Conformer-based encoder**:

### Pipeline

1. **Mel spectrogram extraction** — raw audio → 2D time-frequency representation (time on X, frequency bands on Y)
2. **2D convolutional chunking** — two 2D conv layers group mel features into overlapping chunks and downsample the sequence
3. **Conformer encoding** — a Transformer encoder augmented with a convolutional module processes the soft tokens; outputs contextual embeddings
4. **Linear projection** — projects Conformer outputs into Gemma 4's embedding dimension

![[raw/00-clippings/images/17aae94eb751430bcd236c35847cb5d3_MD5.webp]]

*Audio preprocessing: raw waveform → mel spectrogram → 2D conv chunks → sequence of "soft tokens" ready for the Conformer.*

![[raw/00-clippings/images/468cb5a2efddd03e1798d12d13d9dec5_MD5.webp]]

*Conformer vs. dense Gemma 4 31B architecture: the Conformer is a Transformer encoder (not decoder) augmented with a convolutional module. It produces embeddings, not tokens.*

![[raw/00-clippings/images/974dcc12d97ea391c8325a8f4f9a32fa_MD5.webp]]

*Full audio pipeline: mel spectrogram → Conformer → linear projection → Gemma 4 decoder. Same projection pattern as the vision encoder.*

The Conformer is trained jointly with Gemma 4 to ensure its output embeddings match the LLM's expected distribution.

---

## Related Topics

- [[attention-transformers]] — self-attention, multi-head attention, RoPE, GQA, KV caching
- [[ai-model-architectures]] — Gemma 4 is a worked example of MoE and VLM architecture types
- [[multimodal-models]] — CLIP, BLIP, and the broader vision-language model landscape
- [[audio-processing]] — ASR, mel spectrograms, sampling rates
- [[quantization]] — for running Gemma 4 efficiently; especially relevant for the 26B MoE VRAM tradeoff
- [[gpu-cuda]] — VRAM math for loading sparse MoE weights; the MoE VRAM trap
