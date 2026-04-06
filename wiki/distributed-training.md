# Distributed Training

As models grow beyond billions of parameters, training on a single GPU becomes impossible. Distributed training splits computation, memory, and data across hundreds or thousands of GPUs. This topic covers the key strategies, hardware constraints, and efficiency metrics for large-scale model training.

## Source

- `raw/03-stanford-cs231n/Stanford CS231N.md`

## Why Distribute?

| Model size | Single GPU memory needed |
|-----------|--------------------------|
| 1B parameters | ~8 GB |
| 10B parameters | ~80 GB |

Memory per parameter with Adam optimizer:
- **Weight W[i]** — the parameter itself
- **Gradient dL/dW[i]** — current direction
- **First moment m[i]** — momentum (direction on average)
- **Second moment v[i]** — how trustworthy that direction is

At BF16/FP16: 2 bytes × 4 numbers = **8 bytes per parameter**.
→ 100B params = 800 GB minimum just for weights + optimizer states.

## GPU Hardware: NVIDIA H100

- **80 GB HBM memory** on-chip
- **3,352 GB/s** internal memory bandwidth
- **132 Streaming Multiprocessors (SMs)** — independent parallel compute units
- Each SM has:
  - 128 FP32 cores (256 FLOPs/cycle) — scalar/vector math
  - 4 Tensor Cores (4,096 FLOPs/cycle) — matrix multiply-accumulate
  - Tensor Cores are **16× faster** than FP32 cores — keep operations in matrix form to use them

**Yield and binning:** chips have manufacturing defects; the H100 has 144 SMs but only 132 enabled (disabled defective units). "Binning" = grading chips by quality after testing.

**Tensor Cores operate in mixed precision:** inputs in FP16/BF16/FP8, accumulation in FP32 — fastest path for deep learning.

## GPU Cluster Bandwidth Hierarchy

The Meta Llama 3 cluster architecture shows the real hierarchy:

| Scale | Bandwidth | Technology | Example |
|-------|-----------|------------|---------|
| Inside 1 GPU | 3,352 GB/s | HBM memory | On-chip, fastest |
| 1 server (8 GPUs) | ~900 GB/s | NVLink/NVSwitch | Between GPUs |
| 1 rack (2 servers = 16 GPUs) | ~900 GB/s | NVSwitch domain | Same rack |
| 1 pod (192 racks = 3,072 GPUs) | ~50 GB/s | InfiniBand/Ethernet | Across racks |
| Full cluster (24,576 GPUs) | <50 GB/s | Cross-pod networking | Across pods |

The Llama 3 cluster is organized as: GPU → Server (8 GPUs) → Rack (2 servers) → Pod (192 racks = 3,072 GPUs at 50 GB/s between pods).

**Analogy:** 1 GPU = talking to yourself; 8 GPUs = people in the same room; 3K GPUs = people across a city; 24K GPUs = people across continents on Zoom.

Communication becomes the bottleneck at scale — collective operations (all-reduce) dominate training time at pod scale.

## Parallelism Strategies

### Data Parallelism (DP)

Same model on every GPU; each GPU processes a different mini-batch:
- Forward + backward pass on each GPU independently
- Gradients are synchronized (all-reduce) across all GPUs before the optimizer step
- Simple and effective when the model fits in one GPU

### Fully Sharded Data Parallelism (FSDP / ZeRO)

When the model doesn't fit in a single GPU, shard parameters across GPUs:
- **ZeRO Stage 1:** shard optimizer states
- **ZeRO Stage 2:** shard gradients + optimizer states
- **ZeRO Stage 3:** shard parameters + gradients + optimizer states

FSDP solves **parameter memory** but does NOT automatically solve **activation memory**.

Paper: [ZeRO: Memory Optimizations Toward Training Trillion Parameter Models](https://arxiv.org/pdf/1910.02054)

### Activation Checkpointing

During the forward pass, each layer produces activations needed for backpropagation. Storing all activations is expensive for deep networks.

**Activation checkpointing** saves only a subset of activations ("checkpoints") and recomputes the rest on-the-fly during backprop:
- Trades extra compute (one extra partial forward pass) for large memory savings
- Enables training much deeper networks

### Pipeline Parallelism (PP)

Split model layers across GPUs in stages (Huang et al., "Gpipe"):
- GPU 1: layers 1–N/4
- GPU 2: layers N/4+1 to N/2
- GPU 3: layers N/2+1 to 3N/4
- GPU 4: layers 3N/4+1 to N

**Microbatch scheduling:** mini-batches are split into micro-batches so all stages stay busy simultaneously. Forward pass goes left-to-right, backward pass goes right-to-left.

**MFU impact of 4-way PP with 4 microbatches:**
- Naive (1 microbatch): max MFU = 1/4 = **25%** — only 1 GPU busy at a time
- With 4 microbatches: max MFU = 16/28 ≈ **57.1%** — overlap reduces idle "pipeline bubble"

More microbatches = smaller bubble = better MFU, but more memory for activations. Reference: [Gpipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism](https://arxiv.org/pdf/1811.06965)

### Tensor Parallelism (TP)

Split individual weight matrices across multiple GPUs:
- A matrix multiply A × B is split: each GPU holds a column shard of A and a row shard of B
- Requires synchronization after each layer (all-reduce)
- Best within a single server (NVLink bandwidth)

### Context Parallelism (CP)

For very long sequences (16K–128K tokens), split the sequence across GPUs:
- GPU 1: tokens 1 to L/2
- GPU 2: tokens L/2+1 to L
- Self-attention requires all tokens → GPUs exchange K and V matrices
- Reduces attention computation per GPU; adds communication overhead

Papers:
- [Ring Attention with Blockwise Transformers for Near-Infinite Context](https://arxiv.org/pdf/2310.01889)
- [DeepSpeed Ulysses](https://arxiv.org/pdf/2309.14509)

### ND Parallelism

Real large-scale training combines multiple parallelism strategies simultaneously:
- TP within a server (NVLink)
- PP across servers
- DP across pods
- CP for long contexts

Reference: [The Llama 3 Herd of Models](https://arxiv.org/pdf/2407.21783)

## Efficiency Metrics

### HFU (Hardware FLOPs Utilization)

The fraction of theoretical matmul performance actually achieved in practice:
- H100 theoretical: 989.4 TFLOPS/sec of 16-bit matrix multiplications on Tensor Cores
- In practice: large matrix multiply gets **~80% HFU** on H100
- Smaller matrices (< 4096×4096) achieve significantly less

```
HFU = achieved FLOPs / theoretical peak FLOPs
```
Ignores real overhead — too optimistic for actual training.

### MFU (Model FLOPs Utilization)

How efficiently the model trains end-to-end, including all overhead:
```
MFU = theoretical model FLOPs per step / actual wall-clock FLOPs per step
```

- MFU > 30% → good
- MFU > 40% → excellent
- Large-scale LLM training: typically 30–45%

**Why MFU drops on newer GPUs:** compute grows faster than memory bandwidth. A100→H100 gave ~3.1× FLOPs but only ~2.1× memory bandwidth → memory-bound bottleneck grows.

**Rule:** optimize for MFU, not HFU.

## TPUs

Google Tensor Processing Units:
- Custom ASICs optimized for matrix operations
- Cannot purchase — only rent via Google Cloud
- Less popular ecosystem than NVIDIA GPUs
- NVIDIA and Google are the two leaders in AI training hardware

## Related Topics

- [[gpu-cuda]] — single-GPU hardware fundamentals (H100, tensor cores, compute capabilities)
- [[optimization]] — Adam optimizer requires 4 numbers per parameter (drives memory requirements)
- [[attention-transformers]] — self-attention is quadratic in sequence length; context parallelism addresses this
- [[neural-networks]] — backpropagation and activation memory
