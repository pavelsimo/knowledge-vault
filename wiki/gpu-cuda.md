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

## Related Topics

- [[transformers-library]] — loading models and managing memory
- [[hugging-face]] — model formats and checkpoint downloads
- [[optimization]] — batch size affects GPU utilization during training
- [[convolutional-neural-networks]] — CNN computations run on GPU kernels
- [[attention-transformers]] — attention = matrix multiplies + softmax, all GPU-accelerated
