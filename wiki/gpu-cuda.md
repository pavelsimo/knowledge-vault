# GPU and CUDA

GPUs (Graphics Processing Units) are massively parallel processors that power modern deep learning. CUDA is NVIDIA's programming platform for running computations on their GPUs. Understanding GPU architecture and CUDA is essential for debugging model loading issues and optimizing inference performance.

## Source

- `raw/01-open-source-models-hugging-face/Open Source Models with Hugging Face.md`
- `raw/03-stanford-cs231n/Stanford CS231N.md`

## What is a CUDA Kernel?

A **kernel** is a function that runs on the GPU — highly parallelized across thousands of cores simultaneously. Deep learning operations (matrix multiplications, attention, convolutions) are all implemented as CUDA kernels.

When PyTorch runs an operation:
1. It does **not** send Python code to the GPU
2. It calls pre-compiled **CUDA kernels** (binary machine code) for the specific GPU architecture
3. These kernels are embedded in the PyTorch binary at build time

## GPU Architectures (NVIDIA Compute Capabilities)

Each GPU generation has a **compute capability** code (sm_XX) that identifies its supported features:

| GPU Family | Architecture | Compute Capability | Code |
|------------|-------------|-------------------|------|
| GTX 900 | Maxwell | 5.2 | sm_52 |
| GTX 10xx (Pascal) | Pascal | 6.1 | **sm_61** |
| RTX 20xx | Turing | 7.5 | sm_75 |
| RTX 30xx | Ampere | 8.6 | sm_86 |
| RTX 40xx | Ada Lovelace | 8.9 | sm_89 |
| H100 | Hopper | 9.0+ | sm_90 |

**Personal GPU note:** GTX 1060 = Pascal architecture = sm_61 (compute capability 6.1)

## Common CUDA Error

```
CUDA error: no kernel image is available for execution on the device
```

**Meaning:** The PyTorch build you installed doesn't include compiled kernels for your GPU's architecture. PyTorch wheels only embed kernels for a subset of GPU architectures.

**Fix options:**
1. Install a PyTorch version that supports your GPU
2. Build PyTorch from source for your specific architecture
3. Use CPU inference (slower but always works)

## Model Memory Requirements

Loading a model requires more RAM than the checkpoint size:

```
Required memory ≈ checkpoint_size × 1.1 to 1.3
```

Example:
- `model.safetensors` = 1.62 GB
- Runtime memory needed = 1.62 × 1.3 ≈ **2.1 GB**

The extra memory accounts for:
- Activation buffers
- Optimizer states (during training)
- Framework overhead

## Batch Size and Memory

`batch_size` is a multiplier on memory requirements:
- Larger batch size = more samples processed in parallel = more GPU memory
- If GPU has enough capacity, larger batches improve throughput
- Rule of thumb: double the batch size ≈ roughly double the memory usage

## Model Parallelism (for Very Large Models)

When a model is too large for a single GPU (e.g., LLMs with billions of parameters):

- **Data parallelism:** same model on multiple GPUs, different data batches
- **Tensor parallelism:** split individual weight matrices across GPUs
- **Pipeline parallelism:** split model layers across GPUs
- **Context parallelism (CP):** split the sequence/attention computation across GPUs
  - GPUs exchange K and V matrices (or partial attention results)
  - Each GPU computes attention for its subset of tokens

## Safetensors vs pytorch_model.bin

| Format | Security | Speed | Portability |
|--------|----------|-------|-------------|
| `pytorch_model.bin` | Can execute Python code on load (unsafe) | Slower (deserialization) | PyTorch only |
| `.safetensors` | Cannot execute code (safe) | Faster (memory-mapped) | Multi-framework |

Modern Hugging Face models default to `.safetensors`.

## LLM VRAM Math

The core formula for estimating how much VRAM a model requires:

```
VRAM (GB) ≈ Parameters (billions) × (bits per weight ÷ 8)
```

### Memory per 1B Parameters by Precision

| Format | Bits | GB / 1B params |
|--------|------|----------------|
| FP16 / BF16 | 16 | ~2.0 GB |
| FP8 / INT8 | 8 | ~1.0 GB |
| 4-bit quants | 4 | ~0.5 GB |
| GGUF Q6_K | ~6.6 | ~0.82 GB |
| GGUF Q5_K | ~5.5 | ~0.69 GB |
| GGUF Q4_K | ~4.5 | ~0.56 GB |
| GGUF Q3_K | ~3.5 | ~0.43 GB |
| GGUF Q2_K | ~2.6 | ~0.33 GB |

**Quick rule:** FP16 = 2× model size in GB, FP8 = 1×, 4-bit = 0.5×.

### What Actually Fits by VRAM Size

| VRAM | FP16 | FP8 | 4-bit |
|------|------|-----|-------|
| 8 GB | ~3B | ~6–7B | ~12–13B |
| 12 GB | ~5B | ~10B | ~18–20B |
| 16 GB | ~7B | ~13B | ~25B |
| 24 GB | ~10–12B | ~20B | ~35–40B |
| 48 GB | ~20–24B | ~40B | ~70–80B |
| 80 GB | ~35–40B | ~70B | ~140B class |

### The VRAM Tax: Overhead Beyond Weights

Weights are only part of your VRAM budget. The rest:
- **KV cache** — grows with context length; explodes at 32K, 128K+
- **Activations** — spike under certain execution paths
- **Batching / concurrency** — multiplies usage fast in agent workloads
- **Framework overhead** — varies by runtime (vLLM, TensorRT-LLM, llama.cpp)
- **CUDA Graphs** — reserve extra memory for latency/throughput gains

**Rule of thumb:** add 10–30% on top of weight memory. For long context or high concurrency, plan for even more.

### MoE Memory Trap

Mixture-of-Experts (MoE) models confuse people:
- "8×7B" sounds like 56B, but only a subset of experts activate per token
- **Total parameters** → memory footprint
- **Active parameters** → compute cost (speed)
- You may still need to load all experts into VRAM unless you shard across GPUs

### GGUF Is Runtime-Specific

GGUF memory estimates only apply in llama.cpp-style runtimes. In other frameworks, weights may be dequantized and memory usage can spike dramatically. "Fits in 6 GB" is runtime-specific truth, not universal truth.

## GPU Tier List (2025–2026)

Rankings across NVIDIA, AMD, Apple Silicon, Intel, and Tenstorrent. Scoring criteria: software maturity, VRAM, perf/W & perf/$, multi-GPU scaling, reliability (ECC, thermals), availability, acoustics.

**Quick picks by budget:**

| Budget | NVIDIA | Tenstorrent | AMD |
|---|---|---|---|
| Budget ($2–3K) | RTX 4090 or 3090 (llama.cpp or EXL2 + power-limit) | Wormhole n300d (used units) | Radeon RX 8900 XT |
| Indie ($5–8K) | Dual 5090 / 4090 / RTX 6000 Ada on uniform ×8 Gen4/5 | Twin Blackhole p150c cards in QSFP-800 mesh | AMD PRO W9000 |
| Startup-Lab ($10–15K+) | 4× 5090 / 6000 Ada or 2× A100 80 GB / L40S or 2× RTX PRO 6000 Blackwell | 4× Blackhole p150a mesh (tokens-per-watt king) | 2× MI210 or 4× W9000 |

### S Tier

| GPU | VRAM | Why | Notes |
|---|---|---|---|
| **NVIDIA H100** | 80 GB | FP8/BF16 monster, NVLink/NVSwitch scale, MIG tenancy | PCIe cards anchor 4–8 GPU rigs; SXM needs HGX backplanes |
| **NVIDIA RTX PRO 6000 Blackwell** | 96 GB | Single-slot Blackwell, 4,000 AI TOPS & 1,792 GB/s bandwidth | 600W; demands PCIe 5.0 ×16 + stout airflow/liquid |
| **NVIDIA A100** | 80 GB | Stability benchmark, mature stack, MIG support | Used deals abound; inspect ECC counters pre-buy |
| **Tenstorrent Blackhole p150a** | 32 GB | RISC-V AI SoC, >2.5 TFLOPS/W | QSFP-800 mesh; early kernel porting |

### A Tier

| GPU | VRAM | Why | Notes |
|---|---|---|---|
| **NVIDIA GeForce RTX 5090** | 32 GB | Top consumer perf/$ with 32 GB GDDR7 | No NVLink; "D/DD" cut-down versions exist—check bandwidth |
| **NVIDIA L40S** | 48 GB | Ada datacenter card with FP8, graphics & media blocks | Plays nicely in 4–8 GPU PCIe rigs |
| **NVIDIA RTX 6000 Ada** | 48 GB | ECC workstation champ for dual/quad builds | Mind card length & 12VHPWR routing |
| **NVIDIA A40** | 48 GB | Quiet Ampere with ECC; plentiful used | — |
| **NVIDIA GeForce RTX 4090** | 24 GB | Huge community support; stellar perf/$ for solos | — |

### Consumer Platform: Dual GPU PCIe Layout

For 2-GPU consumer builds (Intel/AMD platform with PCIe bifurcation):

**CPU side:**
- AMD (24 lanes) / LGA1700 (20 lanes)
- 16× PCIe (Gen5) + 2× NVMe
- Intel 20-lane: 8+8+4 chipset (no extra)
- Gen4 x8 = 31.5 GB/s per dir
- Gen5 x8 = 63 GB/s per dir
- Check CPU PCIe bifurcation support

**GPU layout:**
- **GPU 0** — x8 Gen4/5, Primary PCIe Slot (Gen5 ~64 GB/s total), CPU Direct, no sharing
- **GPU 1** — x8 Gen4/5, Secondary PCIe Slot (Gen4 ~32 GB/s total), Shares x16 bifurcation

**⚠ Avoid: GPU Behind Chipset** — only 4 GB/s bottleneck, GPU fails

**Performance reference:**
- GPU 0: 64/32 GB/s (Gen5/4)
- GPU 1: 44/20 GB/s (VAM)
- Chipset: 16 GB/s (RAM) + 8 GB/s (AMD)

**Best practices:**
- Verify x8x8 bifurcation support in BIOS
- Use certified Gen4 riser cables only
- Keep GPUs CPU-direct
- Check manual for lane conflicts

**Critical notes:**
- M.2 slots can downrank PCIe slots — check manual carefully
- Some motherboards disable secondary slot when bifurcation enabled

## Source

- `raw/01-open-source-models-hugging-face/Open Source Models with Hugging Face.md`
- `raw/03-stanford-cs231n/Stanford CS231N.md`
- `raw/00-clippings/GPU Memory Math for LLMs (2026 Edition).md`
- `raw/00-clippings/Thread by @TheAhmadOsman.md`

## Related Topics

- [[transformers-library]] — loading models and managing memory
- [[hugging-face]] — model formats and checkpoint downloads
- [[optimization]] — batch size affects GPU utilization during training
- [[convolutional-neural-networks]] — CNN computations run on GPU kernels
- [[attention-transformers]] — attention = matrix multiplies + softmax, all GPU-accelerated
- [[distributed-training]] — sharding large models across multiple GPUs
- [[quantization]] — how weight precision (FP16, INT8, 4-bit) determines VRAM footprint and speed
