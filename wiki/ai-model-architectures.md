# AI Model Architectures

Modern AI is not a single type of model — it is a family of specialized architectures, each designed around a different task modality or constraint. Understanding which architecture to use, and why, is as important as understanding how to train them.

## Source

- `raw/00-clippings/Thread by @akshay_pachaar 1.md`

## The Eight Specialized Architectures

### 1. LLM — Large Language Model

The dominant architecture for text generation and reasoning.

**Core pipeline:**
1. **Embedding** — convert tokens into dense vector representations
2. **Transformer** — multi-head self-attention + feedforward layers, stacked N times
3. **Response Generation** — decode output token by token via autoregressive sampling

LLMs generate text by predicting the next token given all previous tokens. The transformer's self-attention allows every token to attend to every other token in the context window. See [[attention-transformers]] for full mechanics.

**Examples:** GPT-4, Claude, LLaMA, Gemini

---

### 2. LCM — Large Concept Model

LCMs reason at the level of concepts rather than tokens — operating in a higher-level semantic space that abstracts away surface form.

**Core pipeline:**
1. **Semantic Representation** — map input to concept space rather than token space
2. **Concept Embedding** — compress into conceptual vectors
3. **Advanced Reasoning / Abstract Process** — reason over concepts, not words
4. **Quick Decision** — produce concept-level outputs that can then be decoded to text

The key distinction from LLMs: LCMs work at a level of abstraction above individual tokens, making them potentially more language-agnostic and better at cross-lingual reasoning.

---

### 3. LAM — Large Action Model

LAMs are designed to execute multi-step tasks in the real world or digital environments — not just generate text, but take actions.

**Core pipeline:**
1. **Perception Processing** — parse and understand multimodal inputs (text, screen, sensor data)
2. **Intent Recognition** — determine what the user or task requires
3. **Advanced Reasoning** — plan the sequence of actions needed
4. **Feedback Integration** — incorporate results of previous actions into next steps
5. **Action Execution** — output concrete actions (API calls, UI interactions, robot motor commands)

LAMs close the loop between reasoning and action. They are the architecture behind AI agents that interact with software or physical environments. See [[ai-agents]] for orchestration patterns.

---

### 4. MoE — Mixture of Experts

MoE replaces a single dense feedforward network with many specialized "expert" sub-networks. Only a subset of experts are activated for any given input.

**Core pipeline:**
1. **Input** — token or representation enters the model
2. **Router** — a learned gating network selects the top-k experts for this input
3. **Expert networks** (Expert 1, Expert 2, Expert 3, Expert 4, ...) — run in parallel; only the selected k experts compute
4. **Top-k aggregation** — combine weighted outputs from selected experts
5. **Advanced reasoning / Quantization** — final processing before output

**Why MoE:** the model can have vastly more total parameters than a dense model, but only activates a fraction per token — so compute cost stays comparable to a smaller dense model while capacity increases. GPT-4, Mixtral, and Gemini 1.5 all use MoE.

**The MoE VRAM trap:** MoE models require all expert weights resident in memory simultaneously even though only a few activate per token. A 47B-parameter MoE model may need as much VRAM as a 70B dense model. See [[gpu-cuda]] for VRAM math.

---

### 5. VLM — Vision-Language Model

VLMs combine a vision encoder with a language model, enabling reasoning across images and text.

**Core pipeline:**
1. **Visual Input** — image or video frames
2. **Text Input** — question or instruction
3. **Vision Encoder** — convolutional or ViT encoder extracts visual features
4. **Projection Interface** — adapter that maps visual features into the language model's embedding space
5. **Multimodal Processor** — joint attention over both visual and text tokens
6. **Language Model** — standard transformer decoder
7. **Output Generation** — text, bounding boxes, or structured predictions

The projection interface is the critical bridge — it must align two different embedding spaces (visual and linguistic) so the language model can reason about image content as if it were text. See [[multimodal-models]] for CLIP and BLIP architectures.

**Examples:** LLaVA, GPT-4V, Claude 3, Gemini

---

### 6. SLM — Small Language Model

SLMs are language models optimized for edge deployment — devices with limited memory, compute, and power budget.

**Core pipeline:**
1. **Small Vocabulary** — reduced vocabulary size cuts embedding table memory
2. **Compact Tokenization** — efficient tokenization reduces sequence lengths
3. **Efficient Transformer** — fewer layers, smaller hidden dimensions, attention optimizations (GQA, MQA)
4. **Optimized Embeddings** — quantized or factorized weight representations
5. **Edge Deployment** — run on-device without cloud connectivity

SLMs trade raw capability for efficiency. Common optimizations: weight quantization (INT4/INT8), knowledge distillation from larger models, pruning, and grouped-query attention to reduce KV cache. See [[quantization]] for the full tradeoff landscape.

**Examples:** Phi-3, Gemma 2B, Mistral 7B (small-scale deployment), Apple's on-device models

---

### 7. MLM — Masked Language Model

MLMs learn bidirectional representations by predicting randomly masked tokens given surrounding context — unlike LLMs which predict left-to-right.

**Core pipeline:**
1. **Token Masking** — randomly replace 15% of input tokens with [MASK]
2. **Embedded Input** — full sequence (with masks) embedded into vectors
3. **Left Context + Right Context** — the transformer reads both directions simultaneously
4. **Bidirectional Learning** — attention attends to both past and future tokens
5. **Masked Token Prediction** — output head predicts the original masked token
6. **Fine-Tuning** — the pretrained encoder is fine-tuned with a task-specific head

**Key distinction from LLMs:** MLMs produce bidirectional representations — each token sees the entire surrounding context, not just what came before. This makes them excellent encoders for classification, retrieval, and semantic similarity tasks.

**Limitation:** MLMs cannot generate text autoregressively (they're not trained to predict the next token).

**Examples:** BERT, RoBERTa, DeBERTa

---

### 8. SAM — Segment Anything Model

SAMs are designed for universal image segmentation — given any prompt (point, box, or text), segment the relevant object at any granularity.

**Core pipeline:**
1. **Image Input** — full-resolution image
2. **Image Encoder** — heavyweight ViT encoder runs once to produce dense feature embeddings
3. **Prompt Encoding** — encode user prompts (points, boxes, masks, text) into vectors
4. **Mask Decoder** — lightweight decoder cross-attends prompt embeddings to image features
5. **Feature Embedding** — fuse image + prompt representations
6. **Output Masks** — one or more candidate masks with confidence scores

The design key: the image encoder is the expensive step and runs once. The prompt encoder + mask decoder are fast — they enable interactive, real-time segmentation for arbitrary prompts without re-running the full encoder. This enables applications like one-click segmentation in image editors, medical image annotation, and robot scene understanding.

**Examples:** SAM (Meta), SAM 2 (video extension), Grounded-SAM (text-prompted)

## Architecture Selection Guide

| Need | Architecture |
|---|---|
| Text generation, coding, reasoning | LLM |
| High-level concept reasoning, cross-lingual | LCM |
| Task automation, software/robot interaction | LAM |
| Large-capacity model within compute budget | MoE |
| Vision + language reasoning (image QA) | VLM |
| On-device inference, low latency, offline | SLM |
| Embeddings, classification, search/retrieval | MLM |
| Image segmentation, interactive object selection | SAM |

## Related Topics

- [[attention-transformers]] — shared transformer backbone across LLM, MLM, VLM, SAM
- [[multimodal-models]] — VLM architecture deep dive (CLIP, BLIP)
- [[quantization]] — SLM optimization via weight quantization
- [[gpu-cuda]] — VRAM requirements per architecture type, MoE trap
- [[computer-vision]] — SAM for segmentation; VLM for visual reasoning
- [[ai-agents]] — LAM as the architecture for autonomous agents
