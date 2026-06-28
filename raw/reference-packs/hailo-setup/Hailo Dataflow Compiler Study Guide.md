
A practical reference for compiling neural networks to the Hailo-8 accelerator, covering the full pipeline from ONNX to HEF, how to read the logs, and how to debug common issues.

---

## 1. The Pipeline

```
ONNX  →  translate  →  HAR (FP32)
                        ↓
                        optimize  →  HAR (INT8, quantized)
                                      ↓
                                      compile  →  HEF
```

Three distinct stages, each producing a different artifact:

|Stage|Input|Output|Time|What happens|
|---|---|---|---|---|
|Translation|ONNX|HAR (unoptimized)|seconds|ONNX graph converted to Hailo's internal representation|
|Optimization|HAR + calibration images|HAR (quantized)|10 min – several hours|FP32 weights quantized to INT8 via Adaround|
|Compilation|HAR (quantized)|HEF|10–20 minutes|Weights mapped onto Hailo-8 physical hardware|

**Key insight:** optimization and compilation are independent. Optimization determines accuracy (SNR / dB). Compilation determines speed (FPS / latency). You can iterate on one without redoing the other.

---

## 2. File Types

|Extension|Contents|When you need it|
|---|---|---|
|`.onnx`|Original FP32 model|Initial translation, or to re-quantize with different settings|
|`.har` (unoptimized)|Hailo graph, FP32 weights|Intermediate, rarely kept|
|`.har` (quantized)|Hailo graph, INT8 weights, optimization state|**Keep this.** Lets you recompile in 14 min instead of 1+ hours|
|`.alls`|Model script — user-controllable settings|Your configuration for both optimization and compilation|
|`.hef`|Compiled binary for the Hailo-8|The deployable output|

**Always save the `.har` somewhere persistent.** If it lives in `/tmp`, you lose it on reboot and have to redo the expensive Adaround step.

---

## 3. Quantization: Adaround Explained

Adaround (Adaptive Rounding) is how the DFC converts FP32 weights to INT8.

### The Problem

Naive rounding (to nearest integer) isn't optimal. Sometimes rounding a weight _away_ from the nearest value produces better output because it compensates for rounding errors in neighboring weights.

### The Approach

Adaround operates **layer by layer**, freezing all other layers. For each layer:

1. Run calibration images through the **FP32 model** up to the current layer — record the output (ground truth).
2. Introduce a learnable variable `v` for each weight, between 0 and 1. `0` = round down, `1` = round up.
3. Run the same images through the **quantized layer** with soft rounding.
4. Compute reconstruction loss: how far the quantized output is from the FP32 reference.
5. Optimize `v` via gradient descent to minimize the loss.
6. Snap to hard binary decisions at the end (round up or down).

The key is that the loss is **reconstruction error**, not task loss. No labels needed. The ONNX model is the teacher, the quantized layer is the student.

### Why Layer-by-Layer?

Joint optimization would be a massive non-convex problem. Per-layer decomposition makes it tractable. Downside: it doesn't account for error accumulation across layers — which is why SNR varies across output layers.

### The Annealing Trick

The sigmoid shape controlling `v` is parameterized by `annealing_b`:

- **annealing_b = 20** (hot): gentle slope, weights can explore freely between values
- **annealing_b = 5** (warm): steepens, weights lean toward one side but can still flip
- **annealing_b = 0.5** (cold): nearly a step function, decisions are effectively committed
- **End**: snap to 0 or 1

Annealing comes from metalworking — slow cooling lets atoms settle into ordered low-energy structures. Same idea here: slow commitment lets the algorithm find good rounding decisions instead of getting stuck.

---

## 4. Reading the Logs

### Training progress line

```
Training: 37%|███▋ | 6676/18240 [00:12<00:19, 586.66batches/s,
         round_loss: 9.2104 - annealing_b: 16.2660]
```

|Field|Meaning|
|---|---|
|`37%`|Progress through current layer|
|`6676/18240`|Batch number / total batches for this layer|
|`[00:12<00:19]`|Elapsed / remaining time for this layer|
|`586.66 batches/s`|Throughput — higher is better|
|`round_loss: 9.2104`|Reconstruction error vs FP32 reference (should decrease)|
|`annealing_b: 16.2660`|Temperature — drops from ~20 to ~0 over training|

Total batches per layer = `calibration_images / batch_size × epochs`.

### Block progress line

```
Adaround: 91%|█████████▏| 106/116 [1:25:32<16:01, 96.18s/blocks]
```

Each block = one layer being quantized. YOLO26n has 116 layers. Bigger models have more blocks = longer total time.

### SNR output

```
[info] yolo26n/output_layer1 SNR: 24.86 dB
[info] yolo26n/output_layer2 SNR: 43.98 dB
```

See §5 for interpretation.

### Compilation utilization table

```
| Cluster   | Control Utilization | Compute Utilization | Memory Utilization |
| cluster_6 | 100%                | 48.4%               | 57%                |
| cluster_7 | 25%                 | 6.3%                | 7.8%               |
| Total     | 60.2%               | 26.2%               | 32.3%              |
```

- **Control**: how busy each cluster is with operations (scheduling/routing)
- **Compute**: actual math throughput (this is what limits FPS)
- **Memory**: on-chip SRAM usage
- Imbalance is normal — some layers are just bigger than others
- Low compute utilization means room to improve FPS with `compiler_optimization_level=max`

---

## 5. Understanding SNR (dB)

Signal-to-Noise Ratio, in decibels, measures how closely the quantized layer reproduces the FP32 layer's output.

### Scale

dB is logarithmic — gaps are bigger than they look:

|SNR|Noise energy|Assessment|
|---|---|---|
|20 dB|1%|Noisy, possibly usable|
|30 dB|0.1%|Good|
|40 dB|0.01%|Excellent|
|50 dB+|0.001%+|Near-perfect|

### For YOLO Specifically

- **>30 dB on all layers**: healthy, expect minimal mAP drop
- **25–30 dB on detection heads**: usually fine, NMS is forgiving
- **<25 dB on detection heads**: watch for missed small-object detections
- **19 dB gap between best/worst layer**: normal for YOLO

### The Small-Object Head Is Always the Weakest

Output layers 1/2 handle the finest detection grid (smallest objects). They have:

- Narrowest activation ranges (hardest to quantize)
- Least redundancy
- Most sensitivity to noise

If any layer is going to underperform, it's this one.

### The Real Test

SNR is a proxy. The real test is **mAP on validation data** using the quantized model. If mAP drop vs FP32 is <1–2%, you're fine regardless of SNR numbers. If SNR looks good but mAP is terrible, something else is wrong (calibration mismatch, preprocessing, NMS config).

---

## 6. Optimization Levels

From the DFC user guide:

|Level|Runs|Time|Use when|
|---|---|---|---|
|0|Nothing (no GPU fallback)|Minutes|CPU-only, debugging|
|1|Basic quantization|Minutes|Quick iteration|
|2|+ statistics|~10 min|Lightweight models|
|3|+ Adaround (light)|Medium|Sweet spot for most models|
|4|+ Adaround (aggressive) + finetune + bias correction|Hours|Best accuracy|

**Rule of thumb**: start at level 2 for speed, jump to level 4 if accuracy isn't acceptable. Level 3 is the untested middle — often a good compromise.

**Default auto-selection**: DFC picks level 2 with GPU + 1024 images, level 1 with GPU + fewer images, level 0 with no GPU.

---

## 7. Batch Size Tradeoffs

Batch size affects Adaround's gradient quality, not just speed.

### Calculations

For a calibration set of N images, batch size B, E epochs per block:

```
unique_batches_per_epoch = N / B
batches_per_block = (N / B) × E
total_gradient_updates = batches_per_block
```

### The Quality Floor

Below ~6 unique batches per epoch, Adaround just memorizes the same few batches — rounding decisions become noisy and less generalizable.

### Example with 356 calibration images

|Batch size|Unique batches/epoch|Quality|
|---|---|---|
|8|~45|Excellent|
|16|~22|Good|
|32|~11|OK|
|64|~6|Borderline|
|128|~3|Poor|

### The Fix

If you want large batches (for speed), increase calibration set size. With 1024 images, batch 64 gives 16 unique batches/epoch — back in the "good" zone.

### L2 Cache Sweet Spot

Too-large batches also hurt speed due to L2 cache spills:

- T4: sweet spot ~16–32 (6 MB L2)
- Laptop Ada: ~32–64 (48 MB L2)
- A100: ~32–64 (40 MB L2)
- A100 often slower at 128 than 64 — HBM bandwidth becomes the bottleneck

---

## 8. GPU Selection

Adaround is a training-shaped workload. GPU choice matters enormously.

|GPU|Arch|TF32 (tensor)|L2|Adaround speed on YOLO26n|
|---|---|---|---|---|
|T4|Turing 2018|not supported|6 MB|~2 b/s (slow)|
|RTX 3500 Ada (laptop)|Ada 2023|~50 TFLOPS|48 MB|~50 b/s|
|A10|Ampere 2020|~125 TFLOPS|6 MB|~80 b/s|
|A100 80GB|Ampere 2020|~156 TFLOPS|40 MB|~175 b/s|

**Key insight**: the T4 lacks TF32 tensor cores entirely. On some configurations CPU is faster than T4. Don't assume "GPU is always faster" — verify.

### Verifying GPU Actually Works

Run this before the full compile:

```python
import tensorflow as tf
print(tf.config.list_physical_devices('GPU'))
a = tf.random.normal([8, 224, 224, 3])
b = tf.keras.layers.Conv2D(64, 3)(a)
print('OK:', b.shape)
```

Expected: GPU listed, `Loaded cuDNN version 912xx` in logs, successful conv output.

---

## 9. Common Environment Issues

### `CUDA_VISIBLE_DEVICES=""` Is NOT "show all"

Empty string = hide all GPUs. Unset = show all. Critical distinction:

```python
# WRONG — hides the GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "" if not gpu else str(gpu)

# RIGHT — don't set it, or explicitly set an index
os.environ.pop("CUDA_VISIBLE_DEVICES", None)
# or
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
```

### Subprocess Environment

When calling `hailomz` from Python, don't blindly inherit `os.environ.copy()` on Databricks. Pop:

```python
for k in ("PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP",
         "SPARK_HOME", "PYSPARK_PYTHON", "PYSPARK_DRIVER_PYTHON"):
    env.pop(k, None)
```

But **preserve**:

```python
for k in ("USER", "HOME", "LOGNAME", "TMPDIR"):
    env.setdefault(k, os.environ.get(k, ""))
```

The compiler needs `USER` for metadata.

### Explicit LD_LIBRARY_PATH

Better to define than filter. On Databricks with CUDA installed:

```python
env["LD_LIBRARY_PATH"] = ":".join([
    "/usr/local/cuda/lib64",
    "/usr/local/cuda/extras/CUPTI/lib64",
    "/usr/local/nvidia/lib64",
    "/usr/lib/x86_64-linux-gnu",
])
```

### The "Unable to register cuDNN factory" Warning

```
E0000 cuda_dnn.cc:8310] Unable to register cuDNN factory: Attempting to
register factory for plugin cuDNN when one has already been registered
```

This is a **cosmetic** warning from TF/XLA, not an error. Both TF's stream executor and XLA try to register cuDNN; second one fails silently. Harmless. Ignore.

### The `cuFuncGetName` Warning on Old Drivers

```
Could not load symbol cuFuncGetName.
Error: /lib/x86_64-linux-gnu/libcuda.so.1: undefined symbol: cuFuncGetName
```

Driver is below 535 (CUDA 12.3+ API not available). Symbol is optional profiling, not compute. Upgrade driver to 560+ if possible. Ignore otherwise.

---

## 10. Debug Logging

When things go wrong, enable these in the subprocess environment:

```python
env.update({
    # Hailo DFC
    "LOGLEVEL": "2",                  # 0–3; 2 is warnings+info

    # TensorFlow
    "TF_CPP_MIN_LOG_LEVEL": "1",      # 0=INFO..3=FATAL
    "TF_CPP_VMODULE": "gpu_device=1,dso_loader=1,cuda_driver=1",

    # cuDNN
    "CUDNN_LOGLEVEL_DBG": "1",        # 1=errors only
    "CUDNN_LOGDEST_DBG": "stdout",
})
```

For surgical debugging, add `CUDA_LAUNCH_BLOCKING=1` (makes kernel errors point at actual line) — but remove it after, it serializes everything and slows down runs.

---

## 11. Contexts

The Hailo-8 has limited on-chip memory. Models that don't fit get split into **contexts** — chunks that run sequentially with context switches in between.

### Reading the Partitioning Log

```
[info] Single context flow failed: Recoverable single context error
[info] Using Multi-context flow
[info] Found valid partition to 3 contexts, Performance improved by 13.5%
```

- **Single context**: whole model fits on-chip, lowest latency
- **2 contexts**: common, small switch penalty
- **3+ contexts**: typical for YOLO on Hailo-8, noticeable latency

Each context switch loads new weights/state into the chip. Fewer contexts = faster inference.

### Reducing Context Count

In the `.alls`:

```
performance_param(compiler_optimization_level=max)
resources_param(max_control_utilization=75%)
resources_param(max_compute_utilization=75%)
resources_param(max_memory_utilization=75%)
```

Default is 60% across the board — raising caps lets the compiler pack tighter.

---

## 12. Improving Accuracy (dB)

Ordered from easiest to hardest:

### Increase Calibration Set

Default is 1024+. Below that you're cutting corners. Aim for 1024–2048 representative images. This is the single highest-leverage change.

### Curate the Calibration Set

Oversample hard cases. If 20% of your real data is small objects, but 5% of calibration images have them, the small-object head gets poor quantization.

### Force Sensitive Layers to 16-bit

In the `.alls`:

```
quantization_param([conv61, conv64], precision_mode=a16_w16)
```

Jumps a weak layer from 25 dB to 45+ dB. Costs chip resources — might force an extra context.

### Enable Finetune and Bias Correction

Often skipped by default:

```
model_optimization_flavor(
    optimization_level=4,
    finetune=enabled,
    bias_correction=enabled
)
```

Adds time, recovers 2–5 dB on weak layers.

### Mixed Precision Search

Let the compiler decide:

```
quantization_param(precision_mode=mixed)
```

Automatically promotes the noisiest layers to higher precision.

---

## 13. Iteration Speed

Know which file to start from:

### Starting from ONNX (slow, full pipeline)

- Different optimization level
- More calibration images
- Force specific layers to 16-bit
- Enable/disable finetune or bias correction
- Change batch size for Adaround

**Time: ~1+ hour** (most of it is Adaround)

### Starting from Quantized HAR (fast, compilation only)

- Change `compiler_optimization_level`
- Adjust `max_*_utilization` caps
- Try different `max_contexts`
- Change `performance_mode`
- Modify input/output format conversions

**Time: ~14 minutes** (partitioning + resource allocation + kernel compile)

**Compilation runs on CPU** — doesn't need a GPU. You can iterate on compilation settings on any machine with the DFC installed.

---

## 14. Typical Commands

### Full pipeline from ONNX

```bash
/opt/hailo-venv/bin/hailomz compile \
    --ckpt /path/to/model.onnx \
    --hw-arch hailo8 \
    --calib-path /path/to/calibration/ \
    --yaml /path/to/config.yaml
```

### Compile-only from quantized HAR

```bash
/opt/hailo-venv/bin/hailo compiler \
    --har /path/to/model.har \
    --hw-arch hailo8 \
    --model-script /path/to/model.alls
```

### Python equivalent

```python
from hailo_sdk_client import ClientRunner

runner = ClientRunner.load_har("model.har")
runner.load_model_script("model.alls")
runner.compile()
runner.save_hef("model.hef")
```

### Re-run noise analysis without re-optimizing

```python
runner = ClientRunner.load_har("model.har")
runner.get_noise_analysis()
```

---

## 15. Troubleshooting Quick Reference

|Symptom|Likely cause|Fix|
|---|---|---|
|Adaround at 1 b/s|GPU not actually being used|Check `CUDA_VISIBLE_DEVICES`, run TF GPU probe|
|"Unable to register cuDNN factory"|Cosmetic TF/XLA warning|Ignore|
|`cuFuncGetName undefined symbol`|Driver < 535 on newer CUDA|Ignore, or upgrade driver|
|`KeyError: 'USER'`|Subprocess env too minimal|Preserve USER/HOME/LOGNAME|
|SNR < 25 dB on a layer|INT8 too aggressive for that layer|Force layer to 16-bit|
|Single context fails|Model too big|Normal for YOLO, use multi-context|
|3+ contexts with low FPS|Compiler being conservative|`compiler_optimization_level=max`|
|Adaround slower than expected|Batch size too small|Increase batch, or reduce calibset/epochs|
|mAP terrible but SNR good|Preprocessing or NMS mismatch|Check input format, NMS thresholds|
|T4 slower than CPU|T4 lacks TF32, small batch|Bigger batch, or pick a real GPU|

---

## 16. Key Takeaways

1. **Save the quantized HAR.** It's the checkpoint between optimization and compilation. Lets you iterate on compilation in 14 minutes instead of 1+ hours.
    
2. **Optimization ≠ compilation.** Accuracy (dB) is set by optimization. Speed (FPS) is set by compilation. Independent dimensions.
    
3. **Verify GPU actually works** before committing to a long compile. TF can silently fall back to CPU.
    
4. **Batch size affects accuracy, not just speed.** At small calibration sets, large batches give poor gradient diversity.
    
5. **SNR is a proxy.** The real test is mAP on validation data. >30 dB is usually fine; watch the small-object detection head (lowest SNR).
    
6. **Multi-context is normal** for YOLO on Hailo-8. Don't chase single-context — chase better utilization within multi-context.
    
7. **The T4 is not a real GPU for this workload.** No TF32, tiny L2. A10/A100 give 30–100× speedup.
    
8. **`CUDA_VISIBLE_DEVICES=""` hides all GPUs.** Not "show all." This is the source of most "mysteriously slow" GPU issues.
    
9. **Low utilization in the log doesn't mean the HEF is bad.** It means there's headroom. Try `compiler_optimization_level=max` to use it.
    
10. **Calibration set quality matters more than size, but both matter.** 1024+ representative images is the default target for a reason.