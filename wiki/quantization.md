# Quantization

Quantization is lossy compression for neural network weights — it maps values from a high-precision floating-point range into a smaller range of integers. A well-quantized model can be 4× smaller and 2× faster while retaining 90%+ of the original quality. This is the primary technique behind running LLMs on consumer hardware.

## Source

- [[raw/00-clippings/Quantization from the ground up.md|raw/00-clippings/Quantization from the ground up.md]]

## Why Models Are So Large

LLM parameters (weights) are the dominant memory cost. An 80B model in bfloat16 is ~160 GB. Parameters are mostly small values close to 0 — a distribution that aligns well with where floating-point formats have the most precision.

## Floating-Point Formats

| Format | Bits | Sign | Exponent | Significand | Precision | Range |
|--------|------|------|----------|-------------|-----------|-------|
| float32 | 32 | 1 | 8 | 23 | ~7 sig figs | ±3.4×10³⁸ |
| float16 | 16 | 1 | 5 | 10 | ~3 sig figs | ±65504 |
| bfloat16 | 16 | 1 | 8 | 7 | ~2 sig figs | ±3.4×10³⁸ |
| float8 | 8 | 1 | varies | varies | ~1 sig fig | — |
| float4 | 4 | 1 | varies | varies | very low | — |

**bfloat16** is the standard for LLM training: its wide exponent range prevents overflow, and 2 significant figures is sufficient for learning.

## What Is Quantization?

Quantization maps continuous float values into a smaller set of discrete integers. The core idea: find the right **scale factor** so that your data fits efficiently into the target bit-width.

### Symmetric Quantization

Center the data around 0. Scale factor = `max(|values|) / qmax`.

```javascript
function quantize({ values, bits }) {
    const vmax = Math.max(...values.map(Math.abs));
    const qmax = 2 ** (bits - 1) - 1;
    const scale = vmax / qmax;
    return { values: values.map(v => Math.round(v / scale)), scale };
}

function dequantize({ values, scale }) {
    return values.map(v => v * scale);
}
```

**Downside:** wastes space when data is skewed (e.g., range is -0.89 to +0.16, but symmetric range goes -0.89 to +0.89).

### Asymmetric Quantization

Shift the quantization range to match the actual data distribution. Stores a `zero` offset alongside the scale.

```javascript
function quantize({ values, bits }) {
    const vmax = Math.max(...values);
    const vmin = Math.min(...values);
    const qmax = 2 ** (bits - 1) - 1;
    const qmin = -(2 ** (bits - 1));
    const scale = (vmax - vmin) / (qmax - qmin);
    const zero = qmin - Math.round(vmin / scale);
    return { values: values.map(x => Math.round(x / scale + zero)), scale, zero };
}

function dequantize({ values, scale, zero }) {
    return values.map(x => scale * (x - zero));
}
```

Asymmetric reduces average error ~50% vs symmetric at the same bit width (e.g., 8.5% vs 18% in a 4-bit example).

## Block Quantization

You can't quantize an entire model in one pass — **outlier parameters** (rare but very large or very small values) will skew the scale and crush all other values into a tiny range.

**Solution:** quantize in **blocks** of 32–256 parameters at a time. Each block gets its own scale (+ zero for asymmetric). This contains outlier impact at the cost of storing extra metadata per block.

Trade-off: larger blocks → less overhead, more error. Smaller blocks → more accuracy, more metadata.

## Quality Impact (Qwen 3.5 9B Benchmarks)

### Perplexity (lower = better)

| Format | Perplexity | Delta |
|--------|-----------|-------|
| bfloat16 | 8.186 | baseline |
| 8-bit symmetric | 8.193 | +0.1% |
| 4-bit asymmetric | 8.563 | +4.6% |
| 4-bit symmetric | 8.71 | +6.4% |
| 2-bit asymmetric | 66.1 | +707.5% |

### KL Divergence (lower = better; compares full probability distributions)

| Format | Mean KL Divergence |
|--------|-------------------|
| 8-bit symmetric | 0.0008 |
| 4-bit asymmetric | 0.0593 |
| 4-bit symmetric | 0.0675 |
| 2-bit asymmetric | 2.1447 |

**Takeaway:** 8-bit is nearly lossless. 4-bit has noticeable but acceptable degradation (~90% quality). 2-bit collapses — the model gets stuck in repetition loops and produces no output.

## Speed Impact (tokens/sec)

| Format | M1 Max | H100 |
|--------|--------|------|
| bfloat16 | 19.45 | 106.85 |
| 8-bit symmetric | 32.36 | 141.61 |
| 4-bit asymmetric | 43.32 | 175.70 |
| 4-bit symmetric | 46.05 | 177.06 |
| 2-bit asymmetric | 40.25 | 166.90 |

Quantization is **faster**, not just smaller — primarily because there is less data to move between memory and compute units. 4-bit runs ~2.3× faster than bfloat16 on both hardware types.

## Advanced Methods

- **Post-training quantization (PTQ):** quantize after training (all methods above)
- **Quantization-aware training (QAT):** introduce quantization during pre-training so the model learns parameters that quantize well
- **AWQ (Activation-aware Weight Quantization):** accounts for activation magnitudes when scaling weights
- **GPTQ:** uses second-order information (Hessian) to minimize quantization error per layer
- **GGUF:** a container format + quantization strategy optimized for llama.cpp-style runtimes; memory numbers are runtime-specific

## Related Topics

- [[gpu-cuda]] — VRAM math; how quantization format directly determines how much VRAM is needed
- [[distributed-training]] — quantization used alongside tensor parallelism for very large models
- [[hugging-face]] — model hub hosts quantized checkpoints in many formats
- [[transformers-library]] — loading quantized models via bitsandbytes, AutoGPTQ
