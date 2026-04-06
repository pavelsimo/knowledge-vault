# Transformers Library

The `transformers` library by Hugging Face is a framework-agnostic Python library that provides thousands of pretrained models for NLP, vision, and audio tasks. Its primary abstraction is the `Pipeline`, which handles the full preprocessing → inference → postprocessing workflow.

## Source

- [[raw/01-open-source-models-hugging-face/Open Source Models with Hugging Face.md|raw/01-open-source-models-hugging-face/Open Source Models with Hugging Face.md]]

## Framework Agnosticism

The library is designed to work with multiple deep learning backends:
- **PyTorch** (`torch`)
- **TensorFlow** (`tensorflow`)
- **Flax** (`jax`, `flax`)

This is why PyTorch is not installed automatically — you pick your backend explicitly.

## Pipeline API

The `Pipeline` object is the high-level abstraction for solving tasks end-to-end:

![The `transformers` pipeline wraps preprocessing, model execution, and postprocessing behind one task-level interface.](../raw/01-open-source-models-hugging-face/images/img.png)

*This is why the library feels simple from the outside: one task string hides a lot of modality-specific plumbing underneath.*

```python
from transformers import pipeline

# Example: Automatic Speech Recognition
pipe = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3")
result = pipe(audio_file)
```

The pipeline handles internally:
- Text → token IDs conversion (tokenization)
- Audio → log-mel spectrogram conversion
- Image resizing and normalization
- Postprocessing model outputs into human-readable results

### Batch Processing

```python
# batch_size multiplies memory requirement proportionally
asr(audio_16KHz, chunk_length_s=30, batch_size=4, return_timestamps=True)["chunks"]
```

- `batch_size` controls how many inputs run in parallel
- Larger batch size = more GPU memory used = faster throughput (if hardware allows)

## Tokenizers

A tokenizer converts raw text strings into numerical token IDs that the model understands:

```
"Hello world" → [15496, 995]
```

Key rules:
- Each model has its own tokenizer tied to its vocabulary
- **You cannot safely share tokenizers across unrelated models** (e.g., GPT-2 tokenizer on BERT)
- You **can** share tokenizers between models from the same family with the same vocabulary
- Tokenizers run on the **CPU**, not the GPU

## Model Loading and Memory

- Loading a model from disk means loading its checkpoint (weights + config)
- The model object in memory requires ~10–30% more RAM than the checkpoint file

## Related Topics

- [[hugging-face]] — the platform that hosts models
- [[nlp]] — text pipelines (generation, translation, summarization)
- [[audio-processing]] — audio pipelines (ASR, TTS, classification)
- [[computer-vision]] — vision pipelines (detection, segmentation, depth)
- [[gpu-cuda]] — hardware requirements for running models
