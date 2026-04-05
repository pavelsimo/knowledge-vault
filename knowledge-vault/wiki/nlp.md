# NLP (Natural Language Processing)

NLP covers tasks that involve understanding, generating, and transforming human language. Using the Hugging Face [[transformers-library]], these tasks are accessible through the `Pipeline` API with pretrained open-source models.

## Source

- `raw/01-open-source-models-hugging-face/01_text_generation.py`
- `raw/01-open-source-models-hugging-face/02_translation.py`
- `raw/01-open-source-models-hugging-face/03_sumarization.py`

## Text Generation

Text generation predicts the next tokens given a prompt, used in chatbots, code assistants, and content creation.

```python
from transformers import pipeline
pipe = pipeline("text-generation", model="...")
pipe("Once upon a time")
```

- Open-source chat: https://huggingface.co/chat/

## Translation

Machine translation converts text from one language to another.

- **Facebook NLLB** (No Language Left Behind): supports 200 languages
  - Model: `facebook/nllb-200-distilled-600M`
  - Primarily intended for research in machine translation

## Summarization

Summarization condenses long text into a shorter version while preserving key information.

```python
pipe = pipeline("summarization", model="...")
pipe(long_article_text)
```

## Tokenization

Tokenization is the process of converting raw text into token IDs for the model:

- A **tokenizer** is the model's "dictionary" — it defines how text maps to numbers
- Each model family has its own vocabulary and tokenization scheme
- Tokenizers cannot be shared safely across unrelated model families
- Tokenizers run on the **CPU**

### Why Tokenizers Are Model-Specific

| What works | What doesn't |
|------------|-------------|
| Same model family (e.g., NLLB 600M and NLLB 1.3B) | GPT-2 tokenizer on BERT |
| Same vocabulary and tokenization scheme | NLLB tokenizer on T5 |
| | LLaMA tokenizer on Mistral |

## Related Topics

- [[transformers-library]] — Pipeline API and model loading
- [[hugging-face]] — model discovery and hosting
- [[multimodal-models]] — models that combine text with other modalities
- [[sentence-embeddings]] — converting text to vectors for similarity search
