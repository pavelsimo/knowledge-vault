# Multimodal Models

Multimodal models are AI systems that accept and relate more than one type of data (modality) — such as images and text, or audio and text — within a single model. They power tasks like image captioning, visual Q&A, and zero-shot image classification.

## Source

- `raw/01-open-source-models-hugging-face/11-image-retrieval.py`
- `raw/01-open-source-models-hugging-face/12-image-captioning.py`
- `raw/01-open-source-models-hugging-face/05_zero_shot_audio_classification.py`

## What Makes a Model Multimodal

A model is **multimodal** when it takes more than one type of input — for example:
- Image + text prompt → text answer (Visual Q&A)
- Audio clip + text labels → classification score (CLAP)
- Image → text description (captioning)

## Common Multimodal Tasks

| Task | Description |
|------|-------------|
| **Image captioning** | Generate a natural language description of an image |
| **Image-text matching (ITM)** | Score how well an image and text description match |
| **Visual Q&A** | Answer a question about an image |
| **Zero-shot image classification** | Classify an image using text labels, no task-specific training |
| **Zero-shot audio classification** | Classify audio using text labels (see [[audio-processing]]) |

## Key Models

### BLIP (Bootstrapping Language-Image Pretraining)

Salesforce's BLIP models handle multiple image-language tasks:

- **Image-Text Matching (ITM):** `Salesforce/blip-itm-base-coco`
  - Given an image and a sentence, scores how well they match
  - Used for image retrieval: find the image that best matches a query

- **Image Captioning:** `Salesforce/blip-image-captioning-base`
  - Generates a natural language description for any input image

### CLAP (Contrastive Language-Audio Pretraining)

- **Model:** `laion/clap-htsat-unfused`
- Learns a shared audio–text embedding space via contrastive learning
- Enables zero-shot audio classification with arbitrary user-supplied labels
- See [[audio-processing]] for details on how CLAP works

## Contrastive Learning Principle

The contrastive pretraining approach (used in both CLIP for vision-language and CLAP for audio-language):

1. Collect matched pairs: (image/audio, text description)
2. Train the model to pull matched-pair embeddings **closer** in vector space
3. Train the model to push mismatched-pair embeddings **further apart**
4. Result: a joint embedding space where similarity = semantic alignment

At inference time, you can compare any image/audio against any text description — no fine-tuning required.

## Related Topics

- [[computer-vision]] — vision-only models and tasks
- [[audio-processing]] — audio-only models and tasks (ASR, TTS, CLAP)
- [[nlp]] — text-only models
- [[sentence-embeddings]] — embedding spaces and similarity search
- [[hugging-face]] — hosting and discovering multimodal models
- [[attention-transformers]] — the architectural foundation for most multimodal models
