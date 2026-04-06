# Hugging Face

Hugging Face is the central hub for open-source AI models, datasets, and demos, providing infrastructure for discovering, sharing, and running machine learning models across all modalities (text, audio, images, video).

## Source

- [[raw/01-open-source-models-hugging-face/Open Source Models with Hugging Face.md|raw/01-open-source-models-hugging-face/Open Source Models with Hugging Face.md]]
- [[raw/01-open-source-models-hugging-face/helpers.py|raw/01-open-source-models-hugging-face/helpers.py]]

## Repo Helper Utilities

The shared `helpers.py` file is the glue code for the hands-on Hugging Face examples. It does not introduce new modeling ideas; it standardizes visualization so the task scripts can focus on inference.

- [[raw/01-open-source-models-hugging-face/helpers.py|raw/01-open-source-models-hugging-face/helpers.py]] - converts Matplotlib figures to PIL images, overlays one or many segmentation masks on source images, and renders normalized depth maps with optional side-by-side comparisons and color bars.

## Model Hub

- Models are hosted as repositories containing weights, configs, and tokenizer files
- Models can have multiple **checkpoints** — snapshots of saved weights at different training stages
- Loading a model technically means loading a checkpoint (pre-trained weights + configuration)
- Depending on hardware, you may not be able to run the largest checkpoints

### Model Weight Formats

| Format | Notes |
|--------|-------|
| `pytorch_model.bin` | Legacy format; serialized PyTorch checkpoint via `torch.save()` |
| `.safetensors` | Modern format; safer (no arbitrary Python execution), faster (memory-mapped), portable across frameworks |

- A loaded model needs ~10–30% more memory than the raw checkpoint file size
  - Example: `model.safetensors` = 1.62 GB → ~2.1 GB RAM needed at runtime

## Finding Models for Tasks

Hugging Face organizes models by task type:
- [Chat Completion](https://huggingface.co/docs/inference-providers/en/tasks/chat-completion)
- [Feature Extraction](https://huggingface.co/docs/inference-providers/en/tasks/feature-extraction)
- [Automatic Speech Recognition](https://huggingface.co/docs/inference-providers/en/tasks/automatic-speech-recognition)
- [Text to Video](https://huggingface.co/docs/inference-providers/en/tasks/text-to-video)

## Leaderboards and Evaluation

- **[Open LLM Leaderboard](https://huggingface.co/open-llm-leaderboard)** — tracks, ranks, and evaluates open LLMs and chatbots
- **[LM Arena](https://huggingface.co/spaces/lmarena-ai/chatbot-arena)** — crowdsourced rankings across LLMs on versatility, linguistic precision, and cultural context

## Pretrained vs Fine-tuned Models

- **Pretrained models** — trained from scratch on large corpora by big companies with significant compute
- **Fine-tuned models** — pretrained models further trained on a specific task or domain
- **Distilled models** — compressed versions of larger "teacher" models, trained on the teacher's outputs rather than raw human data; designed to be faster and cheaper while retaining accuracy

## Chat Interface

- Chat with open-source models at: https://huggingface.co/chat/

## Notable Models

| Model | Purpose |
|-------|---------|
| `openai/whisper-large-v3` | Automatic speech recognition |
| `facebook/nllb-200-distilled-600M` | Machine translation (200 languages) |
| `facebook/detr-resnet-50` | End-to-end object detection |
| `Zigeng/SlimSAM-uniform-77` | Segmentation mask generation |
| `Intel/dpt-hybrid-midas` | Depth estimation |
| `Salesforce/blip-image-captioning-base` | Image captioning |
| `Salesforce/blip-itm-base-coco` | Image-text matching/retrieval |
| `laion/clap-htsat-unfused` | Zero-shot audio classification |
| `sentence-transformers/all-MiniLM-L6-v2` | Sentence embeddings |

## Related Topics

- [[transformers-library]] — the Python library for using Hugging Face models
- [[nlp]] — text-based tasks and models
- [[audio-processing]] — audio-based tasks and models
- [[computer-vision]] — vision-based tasks and models
- [[multimodal-models]] — cross-modal models
- [[sentence-embeddings]] — embedding models
