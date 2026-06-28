---
title: "The Detailed Explanation of Self-Attention in Simple Words"
source: "https://medium.com/@manindersingh120996/the-detailed-explanation-of-self-attention-in-simple-words-dec917f83ef3"
author:
  - "[[Maninder Singh]]"
published: 2025-04-01
created: 2026-04-22
description: "The attention mechanism is one of the most groundbreaking concepts in deep learning. It fundamentally changes how neural networks process in"
tags:
  - "clippings"
---
The attention mechanism is one of the most groundbreaking concepts in deep learning. It fundamentally changes how neural networks process information by allowing models to selectively focus on the most relevant parts of the input.

However, attention is not a new concept. Bahdanau et al. (2014) first introduced the concept of attention in their paper *“Neural Machine Translation by Jointly Learning to Align and Translate,”* three years before the Transformers were introduced in the seminal 2017 paper *“Attention Is All You Need.”* Despite its early existence, attention gained widespread recognition and adoption only after Transformers demonstrated its full potential. Today, State-of-the-art large language models (LLMs) like ChatGPT, DeepSeek, LLaMA, (decoder-only), BERT (encoder-only),and others **rely on the Transformer architecture, which is based on the self-attention mechanism, to process information and generate content efficiently and accurately.**

I first encountered the attention mechanism while working on a solution that involved fine-tuning encoder-based LLMs like BERT. This sparked my curiosity about how these models works internally, and later, the rise of ChatGPT further deepened my interest in Transformer architectures. Over time, I worked on several projects, including building a Transformer-based translation model from scratch, developing text generation models from scratch, Various RAG and Agents based projects and fine-tuning LLMs, which helped me gain a deeper understanding of attention mechanisms.

In this article, I will break down the self-attention mechanism in the simplest way possible, based on my exploration of the 2017 paper. We will also discuss why attention initially had limited impact and how Transformers revolutionized its usage, making it the foundation of modern deep learning models

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*OLdgDkGOEKJQGXvBqHY5kw.gif)

> This article may be lengthy and repetitive in some sections, as I’ve aimed to explain a single concept from multiple perspectives.

Below is the index of the blog, allowing you to jump directly to the section that best suits your needs.

1. **The Role of Attention Before Transformers**
2. **How Transformers Revolutionised Attention**
3. **Let’s Understand ‘The Self-Attention’**  
	\- What is self-attention  
	\- Why do we need self-attention?
4. **How Does Self-Attention Work?**  
	\- Intuition behind self-attention
5. **The Three steps of Self-Attention (*Mathematical Explanation*)**  
	\- Quick Refresh on Vector Dot Product
6. **Recapping our learning so far**
7. **Understanding Query, Key and Value in Self-Attention using Example**
8. **Introduction of Trainable Parameters**
9. **Why Do We Scale the Attention Scores?**
10. **Multi-Head Attention: To get better understanding**

Before jumping straight into explaining attention architecture, I want to first take a step back and give you a little information on the history of attention mechanism — how it was initially used in RNNs, what challenges led to the rise of Transformers, and what makes attention in Transformers fundamentally different from earlier approaches. By doing this, I hope to build a strong foundation for understanding self-attention while also highlighting its incredible potential.

> \*I have used terms *(RNNs and it’s variants)* and *(Sequential Models)* interchangebaly in the following paragraphs.

## The Role of Attention Before Transformers

Before the rise of Transformers, attention mechanisms were sometimes **used as an auxiliary component in deep learning architectures**, particularly within Recurrent Neural Networks (RNNs) and it’s variants and even if used as a main component in Sequence-to-Sequence (Seq2Seq) models, it was **limited by the inefficiencies of Sequential Models.** These early implementations helped models focus on important parts of input sequences, improving performance in applications like machine translation, speech recognition, and image captioning. However, attention was still constrained by the limitations of RNNs, which led to several challenges:

1. **Sequential Models Process Data Sequentially — and That’s a Problem  
	**RNNs process text one word at a time, passing information from one step to the next. This means:
- They can’t handle long-range dependencies well — as the sequence gets longer, earlier words lose their influence due to vanishing gradients.
- They are slow because each step depends on the previous one, making them hard to parallelize.
- Scaling them up for massive datasets is a nightmare because computation happens step by step instead of all at once.

**2\. Attention Was Expensive in Early Models**  
When attention mechanisms were first introduced in RNN-based models, they used `**additive**` or `**multiplicative attention**` to determine which words were most relevant, this approcah can lead to problems like:

- As sequences got longer, attention calculations became computationally expensive.
- Scaling this to large datasets required way too much processing power, making it impractical for modern deep learning needs.

> `Even though self-attention in Transformers is also expensive with complexity of O(n²) but it benefits from parallelization.`

**3\. Cross-Attention vs. Self-Attention**

- In RNN-based models, attention was mostly cross-attention — it computed scores between the encoder hidden states and the decoder states *(think of it as the decoder looking back at the encoder to decide what to focus on)*.
- But because this attention mechanism was still tied to RNNs, it inherited all their inefficiencies — meaning it couldn’t be parallelized efficiently and still struggled with long-range dependencies.

So, while attention was helpful, it wasn’t enough to fix the fundamental problems of RNNs and it’s variants. That’s where Transformers changed the game with self-attention, allowing models to process entire sequences in parallel and capture relationships across words — no matter how far apart they are.

> **Quick Favor 🙂: If you find this article helpful, consider following me, clapping 👏, or sharing it with others who might benefit. Thank you!. Let’s get back to the article**

## How Transformers Revolutionized Attention

The Transformer architecture completely changed the game by making attention the foundation of the model, rather than just an extra feature. This shift was introduced in the 2017 paper *“Attention Is All You Need,”* which brought in some key innovations that made deep learning models more powerful and efficient.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Q770rwUbk3oKBoGT3LbGNQ.gif)

Following are the key componenets of Transformer based models:

### 1\. Self-Attention: The main Brain

Before Transformers, Traditional Seq2Seq models primarily used cross-attention, where the decoder attended to encoder states. Transformers made self-attention the primary mechanism, allowing every token to attend to all others within the same sequence. This led to some major advantages:

- The model could easily capture long-range dependencies — even words that appear far apart in a sentence.
- All tokens could be processed at once, making computation faster and highly parallelizable on GPUs/TPUs.
- The model could dynamically adjust its focus based on different parts of the input, improving understanding.

### 2\. Multi-Head Attention

Rather than using just one attention mechanism, Transformers introduced multi-head attention — multiple attention mechanisms running in parallel. Each attention head focuses on a different aspect of the input, such as:

- Syntax relationships (e.g., how words like subjects and verbs relate).
- Semantic meaning (e.g., understanding words in context).

By allowing multiple attention heads to process different information simultaneously, Transformers are able to build richer and deeper representations of given language in training data.

### 3\. Positional Encodings to preserve word order

Since Transformers process all tokens simultaneously, they don’t inherently know word order like RNNs do. To fix this, they use positional encodings, which:

- Tell the model where each word appears in a sequence.
- Help distinguish between identical words in different positions (e.g., “She saw a dog” vs. “A dog saw her”).

Positional encodings inject this information using mathematical patterns, ensuring the model understands word placement and sequence structure Without which, a Transformer would just see a bag of words with no structure!

### 4\. Stacked Layers for deep Learning

Transformers don’t just use one self-attention layer — they stack multiple layers along with feed-forward networks. This allows them to:

- Capture deeper contextual meanings across layers.
- Learn abstract patterns as information flows through the network.
- Avoid the vanishing gradient problem through residual connections and layer normalization that made deep RNNs hard to train.

This combination of self-attention, multi-head attention, positional encodings, and deep layering is what makes Transformers so powerful. They can process large datasets efficiently, handle long-range dependencies, and capture nuanced language features — all while being highly parallelizable.

## Let’s Understand ‘The Self-Attention’

Now that we’ve covered the basics of self-attention — its role, a bit of its history, and why it’s so important — let’s shift our focus back to the main goal of this article: **understanding the intuition and mathematics behind self-attention in Transformers.**

In the next sections, I’ll break down **how self-attention works mathematically** and how it enables Transformer models to achieve **state-of-the-art performance** across various tasks. Our primary focus will be on the **Multi-Head Attention** component of the Transformer network, as introduced in the groundbreaking 2017 paper *“Attention Is All You Need.”* You can see this highlighted in the section of the image below.

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*wCA8Vob6W3KR4iJymWGfag.png)

`Let’s start with the definition of the attention first:`

### What is Self-Attention?

Self-attention helps a model understand which parts of a sentence are important when making predictions. It does this by computing three types of vectors for each word in the sentence:

- **Query (Q) Vector:** Represents the current word’s perspective — **what it wants to focus on in the sentence.**
- **Key (K) Vector:** Represents **how relevant each word is** when compared to a query. It is used to compute similarity scores.
- **Value (V) Vector:** Contains the actual word representation, which is weighted based on attention scores **to create the final contextualized word representation.**

These vectors allow the model to compute attention scores, determining how much focus each word should give to others, ultimately improving context understanding

> **Quick Favor 🙂: If you found this article helpful, consider following me, clapping 👏, or sharing it with others who might benefit. Thank you!. Let’s get back to the article**

### Why Do We Need Self-Attention?

For explaining Self-Attention I will be Considering the following example sentence through-out the article:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*JKjgv92zjFFeHfuDA8FlEw.png)

What does the word **“bank”** refer to? Is it a **financial institution** or the **edge of a river**?

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*ZFnFgvSVf_5l-JRuma30mA.gif)

For humans, it’s easy to understand that “bank” refers to a **riverbank** because of the surrounding words like “swam” and “river.” But for computers, understanding this meaning is difficult because the word “bank” can have multiple meanings.

If the sentence is changed to:

***“I drove across the road to get to the other bank,”***

the word “bank” now would likely refer to a financial institution. This example illustrates how the **meaning of a word depends on its context within a sentence.**

> The self-attention mechanism is designed to capture this contextual information by allowing a model to weigh the influence of neighboring words on a given word. This process enhances the meaning of the word by considering its surroundings.

## How Does Self-Attention Work?

As shown in **Figure below**, self-attention is represented as a **black box** inside the Transformer model. Before we apply self-attention, we perform two key steps:

1. **Tokenization:** Breaking a sentence into smaller parts called tokens. There are different ways to do this, but for simplicity, we will separate each word by spaces, as shown in image below.
2. **Word Embedding:** Computers do not understand words- they only work with numbers. To convert tokens in to a form that computers can process, we use word embeddings `(In the original paper, the Transformer model uses learned embeddigns which learns embeddings from scratch throughout the traing process, rather than relying on pre-trained embeddings like Word2Vec or GloVe.)>`
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Gd6nqg1uHAHw3Fcz2ilLtQ.gif)

One important thing to note:

**Word vectors are not just random numbers.** They carry **semantic and contextual meaning**, which means words with similar meanings are placed **closer together** in the numerical space. For example, in an embedding space, words like **“king” and “queen”** or **“river” and “stream”** will be positioned near each other because they have related meanings.

### Intuition Behind Self Attention Mechanism

Now the Question arrises that how can we adjust the vector representation of the word **“bank”** so that, in a given sentence, it moves closer to words like **“river”** and **“canal”** (indicating a water body) instead of words related to **financial institutions**?

👉 This is exactly the job of the **self-attention mechanism**.

### How does self-attention help? (layman-friendly overview)

To give a simple, **layman-friendly overview of what’s happening inside the black box** shown in the image above:

1. It takes the **word vectors** as input.
2. It **assigns different weights** to the surrounding words based on their importance in the sentence using Query-key interactions.
3. Self-attention then computes contextualized representations by dynamically weighting word relationships in a sentence. The original word vector remains unchanged, but the output embeddings reflect contextual meaning.

As a result, after applying **self-attention**, the model better understands the sentence. It recognizes that **“bank”** in this case refers to a **riverbank** and not a **financial institution**.

This is the core idea behind self-attention — it helps the model understand words **in context**, making language processing much more accurate.

## Let’s explore the Black Box Now: The Three steps of Self-Attention

Inside the black box of self-attention, the process consists of three main step, which I will explain in depth one-by-one:

1. Compute **raw attention scores** by taking the dot product of the **Query (Q) and Key (K) vectors** for each word pair
2. Normalisation of Attention Scores using by Applying **Softmax** to the attention scores to convert them into a probability distribution, determining how much focus each word should receive
3. Multiply the attention scores (from Softmax) with the **Value (V) vectors** to obtain a weighted sum, creating a **contextualized representation** of each word.

This can be Visualised as below.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*zWKQUVM3PV5CmF8P3CEFhw.gif)

Before diving into each step in depth, let’s quickly refresh our memory on the **Vector Dot Product**, as it plays a key role in **self-attention**.

### Quick Refresh on Vector Dot Product

The **dot product** is a mathematical operation that helps measure the **similarity** between two vectors.

Imagine we have **three vectors**: **A, B, and C, as shown in the image below**.

- If **DotProduct(A, B) = 10** and **DotProduct(A, C) = -6**, this means **A and B** are **more similar** than **A and C** because **10 is greater than -6**.
- If two vectors are **perpendicular**, their dot product is **0**, meaning they are **completely unrelated**.
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*ASYzBd66gHR63KU2BMbknw.jpeg)

This concept is important because the **self-attention mechanism** relies on the **dot product** to compute **attention scores** — which determine how much **focus** a word should have on other words in a sentence.

## Step 1: Dot Product Calculation for Self-Attention

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*UTAtCCSLD5LtMwT0ezPUVA.jpeg)

Before we compute attention, we first convert each word in a sentence into a **vector representation**. These vectors capture **semantic meaning** and are typically high-dimensional.

For example, each word might be represented as a **\[1 × 100\]** vector, meaning it has **100 numerical values** that encode its meaning based on a learned embedding space or pre-trained embeddings.

To determine how much focus one word should give to another, we compute **attention scores**. This is done using the **dot product** between every possible pair of words — including a word with itself.

📌 *\[Below attached animation can help better understand the process\]*

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*TInd-ZmpKZUVcw0mMAuPCw.gif)

> **NOTE:** The attention scores *s₁₁,s₁₂ … s₁ₙ* here are single scaler values as dot product between *Vₙ* and *Vₙᵗ* is as *\[1x100\]\[100x1\]*. But S₁ is the vector contaning the simillarity information of S₁ with all other words in a sentence.

Now, why to use the **dot product**?

- The **dot product measures similarity** between two vectors.
- A **higher dot product value** means two words are **more related** in the given sentence.

Let’s take our sentence of interest:

➡️ **“I swam across the river to get to the other bank.”**

- The dot product between “bank” and “swam” or “bank” and “river” will be high, indicating a strong relationship.
- The dot product between “bank” and “other” might be lower since “other” doesn’t contribute much meaning in this context.
- If “bank” appeared in another sentence like “I deposited money at the bank,” its dot product with “money” or “deposited” would be higher instead.
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*wzFDUP_FaRDg4z2qPQX-FQ.jpeg)

> This **first step in self-attention** helps the model **identify key word relationships** in the sentence before moving to the next stages of processing.

Now as you can observe, here word river is haviong very high dot product score with the word bank.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*YACaInUj1QOqEJPmvS6lZQ.jpeg)

Here in above plot S₁ represents the first row S₂ represents row 2 and so on. and each element of score ***S₁*** or other represent the each box of row.

> One important point to note is that in the **“Attention Is All You Need”** paper, the authors **did not use pre-trained word embeddings**. Instead, **they learned word embeddings from scratch during training**.
> 
> This is exactly the case with **LLMs like LLaMA, GPT, or BERT**, which **do not use fixed pretrained word embeddings**. Instead, modern LLMs **learn their embeddings dynamically** during training. The **embedding layer** is **randomly initialized**, and through **backpropagation**, the model adjusts these embeddings based on **context**.
> 
> Unlike static word embeddings (e.g., Word2Vec, GloVe), these embeddings **change dynamically** depending on surrounding words, ensuring context-awareness.
> 
> Similarly, **query, key, and value (QKV) matrices** in the attention mechanism are also **randomly initialized** and learned during training. This allows the model to generate **contextualized word representations**, meaning a word like **“bank”** will have **different embeddings** depending on whether it appears in **“river bank”** or **“bank account”**.

## Step 2: Normalizing attention score using Softmax

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*8-meqZa_4xc7iButwCw7Tw.gif)

Animation to represent the corresponding weights obtained after Step 2

In the previous step, we computed the **raw attention scores** by taking the **dot product** between word vectors. However, a key question arises:

> ***🤔 Why do we need to normalize these scores?***

👉 The reason is that the dot product values can vary significantly in scale. Some scores may be very large, while others may be very small, leading to:

1. **Unstable gradients** — If the scores are too large, the softmax function can produce **highly skewed probabilities**, making the model harder to train.
2. **Inefficient learning** — Large variations in scale can cause some words to dominate attention while others contribute little, affecting **contextual learning**.

> **Quick Favor 🙂: If you found this article helpful, consider following me, clapping 👏, or sharing it with others who might benefit. Thank you!. Let’s get back to the article**

### How do we normalize the scores?

To address this, we **apply two transformations**:

1. **Scaling** *(will explain intuition about this in latter section of the article)* — We divide the raw attention scores by ***√dₖ***, where *dₖ* is the dimension of the key vectors. This prevents large dot products from producing extreme values.
2. **Softmax function** — We use the **Softmax function** to normalize raw attention scores. Given a set of scores in a row, Softmax transforms them as follows:This ensures that all attention scores for a given word **sum to 1**, converting them into a probability distribution.

![](https://miro.medium.com/v2/resize:fit:2000/format:webp/1*fvOh_KqfF4cR-64-pky88Q.jpeg)

Image explaining step 2

where:

- Sᵢⱼ represents the **raw attention score** between **word *i* (query) and word *j* (key)**.
- The denominator ensures that the sum of all attention scores in a row is **1**, making them interpretable as probabilities.

### Interpreting the normalised scores as Weights

After applying Softmax, the **normalized attention scores become the attention weights**. We denote these weights as **Wᵢⱼ**, where:

- `*Wᵢⱼ*` represents **how much importance word** `***j***` **has when computing the representation of word** `***i***`.
- Each weight is derived from its corresponding raw score Sᵢⱼ as shown in the image above.
- The weights satisfy: **∑ⱼ *Wᵢⱼ = 1***
- ensuring that they act as a **probability distribution**.

Thus, ***W₁₁*** is the weight corresponding to ***S₁₁***, ***W₁₂*** to ***S₁₂***, and so on.

**Using These Weights in Self-Attention  
**Once we have the attention weights, we use them to **weight the original word vectors.** This means each word vector is recalibrated based on its contextual importance.

In the next step, we will see how these weighted word vectors are combined to generate the final contextualized representation of each word in the sentence.

## Step 3: Computing the Contextualised Word Representation

Now that we have computed the attention weights in the previous step, these weights will be used to scale the original word vectors. This step ensures that each word vector is adjusted based on its relationship with other words in the sentence.

### What Are the Original Word Vectors?

The **original word vectors** refer to the set of vectors **V**, which represent each word in the input sequence. In self-attention, we denote these vectors as **V (Value vectors)**. These vectors are the **same as the initial word embeddings** but will be **contextualized** through the weighting process.

### How Are Word Vectors Weighted?

The self-attention mechanism computes new, contextualized word representations by applying the attention weights (W) to the original word vectors (V). This is done using the following matrix operations:

## Get Maninder Singh’s stories in your inbox

Join Medium for free to get updates from this writer.

***Y=W⋅V***

Expanding this equation:

***Yᵢ=* ∑ⱼ *WᵢⱼVⱼ***

📌 As shown in the Animation below

where:

- *W* is the **attention weight matrix**, where each row *Wᵢ* represents the attention weights for word ***i***.
- ***V*** is the **Value matrix**, where each row represents the vector of a word.
- ***Yᵢ*** is the new **contextualized word representation** for word ***i***.

This means that for each word ***i***, its final representation is a weighted sum of the value vectors of all words in the sequence.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*cwlal9-TS46sHyF3m_iOow.gif)

Animation to explain step 3 of Self-Attention

### What Does This Actually Mean?

For each output *Y* ***ᵢ***, the contextualized representation of word ***Vᵢ*** is obtained by taking into account:

- The **influence of *V₁*** weighted by ***Wᵢ₁***
- The **influence of *V₂*** weighted by ***Wᵢ₂***
- …
- The **influence of *Vₙ*** weighted by ***Wᵢₙ***

This process is repeated for **all** words, creating a new set of vectors (***Y₁* to *Yₙ***), where each word representation now `**incorporates contextual information from surrounding words**.`

### Why Does This Matter?

Initially, the word vectors (V) only represent words individually, without considering their meaning in a sentence. However, after applying self-attention:

✅ The word vectors are updated based on their relevance to other words in the sentence.

✅ Words that were pointing in different directions in vector space now shift towards a direction influenced by their neighbors.

✅ `The model now understands the context in which the word is used.`

For example, the word **“bank”** in the sentence **“I sat near the river bank”** will shift closer to words like **“water”** and **“river”**, distinguishing it from the **“bank”** in **“I deposited money in the bank”**, which would move closer to financial terms.

This is how self-attention creates contextualized word representations, allowing deep learning models to better understand meaning based on context.

## Recapping our learning so far

That’s it! that’s the intuition behind the self attetnion in transformers, to summarize the process once again:

1️⃣ **Tokenization** — The input sentence is broken down into individual tokens (words or subwords).

2️⃣ **Word Embeddings** — Each token is converted into a numerical representation using Word embeddings.

3️⃣ **Applying Self-Attention** — The attention mechanism is used to determine how much influence each neighboring word has on a given word. This helps in modifying the original word vectors `to obtain contextualized representations.`

4️⃣ **Steps in Self-Attention:**

- **Step 1:** Compute attention scores using the **dot product** between word vectors `(query and key) ` which are transformerd versions of the original word embeddings.
- **Step 2:** **Normalize** the scores (typically using softmax) to get attention weights.
- **Step 3:** Use these attention weights to scale the original word vectors (value vectors) which are obtained from the original word embeddings and obtain the final contextualized word representations.

Through this process, the model `**dynamically adjusts** ` each word’s representation based on its `**context**`, ensuring that words like **“bank”** are interpreted correctly based on the surrounding words.

> This ability to understand context **efficiently and accurately** is what makes self-attention such a game-changer in NLP and allow the model to adjust word meanings based on the context of the entire sentence, making Transformers incredibly powerful for tasks like language translation, text generation, and question answering.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*LWj6JSTt6YRZkdLtcxXr5w.jpeg)

Self Attention Complete Mechanism

## Understanding Query, Key, and Value in Self-Attention using Example

Even though I’ve already provided a quick revision earlier in the article, I’m revisiting the process now to explain it in terms of **Query (Q), Key (K), and Value (V)** — the fundamental components of the self-attention mechanism. This will help us pinpoint where the **trainable parameters** exist in self-attention.

`If you already understand the core intuition, feel free to skip this section till **the section of introduction of trainable paramters**!`

Suppose we have a sentence consisting of three words, which, after tokenization and vectorization, are represented as **V₁, V₂, and V₃**. Our objective is to compute the **attention score for V₂** using the self-attention mechanism, ultimately obtaining its **contextualized representation**.

In this scenario:

- ***V₂* acts as the query (Q₂)** — the word we are focusing on.
- ***V₁, V₂, and V₃* serve as keys *(K₁, K₂, K₃)*** — words that we want to compare with the query to determine their relevance.

The goal is to measure **how closely each key vector *(K₁, K₂, K₃)* aligns with the query vector (Q₂)**. This will help determine which words influence V₂ the most.

### Step 1: Computing Raw Attention Scores

To achieve this, we calculate the **dot product** between the query vector of V₂ and each key vector in the sequence, producing the following attention scores:

*S₂₁= Q₂⋅K₁*

*S₂₂= Q₂⋅K₂*

*S₂₃=Q₂⋅K₃*

where ***S₂₁, S₂₂, and S₂₃*** represent the similarity scores between V₂ and the words **V₁, V₂, and V₃**, respectively.

At this stage, these raw scores indicate the degree of similarity between V₂ and the other words in the sentence. The next steps will involve scaling, normalizing, and weighting these scores to refine the attention mechanism further.

![](https://miro.medium.com/v2/resize:fit:2000/format:webp/1*mZXOrT72Tzk31TvV89ytWQ.png)

Visual Representation of the complete Process

### Substep of normalising the scores

Before normalizing the attention scores, we apply scaling to stabilize training. This is necessary because the dot product values can grow large as the vector dimensions increase, leading to high variance in gradients. To address this, we divide each score by the square root of the key vector dimension (*dₖ*):

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*YuoB3wtSedTSm_G8hPgC_w.png)

where **dₖ** represents the **dimension of the key vectors**. This scaling ensures that the magnitude of scores remains controlled, preventing extremely large values that could negatively impact the softmax function in the next step.

### Step 2: Normalizing the Scores

Once the scores are scaled, they are passed through a **softmax function** to normalize them into probabilities that sum to **1**. This converts the raw similarity scores into attention weights, ensuring that words receive appropriate emphasis based on their relevance.

***Wᵢⱼ=softmax(Sᵢⱼ)***

After applying softmax, the resulting values ***W₂₁, W₂₂*** and ***W₂₃*** represent the final attention weights assigned to each word with respect to ***V₂***.

### Step 3: Computing the Contextualized Representation

Now that we have the attention weights, we use them to compute the **contextualized representation of V₂**. `At this stage, the original word vectors ***V₁, V₂,* and *V₃*** act as **Values (V)**, which are weighted accordingly to incorporate contextual influence.`

The final contextualized vector ***Y₂*** is obtained by computing the weighted sum of the value vectors:

***Y₂=W₂₁V₁+W₂₂V₂+W₂₃V₃***

This new vector ***Y₂*** represents the word ***V₂*** in its contextualized form, meaning its representation now reflects the influence of surrounding words in the sentence.

> **Quick Favor 🙂: If you found this article helpful, consider following me, clapping 👏, or sharing it with others who might benefit. Thank you!. Let’s get back to the article**

## Introduction of trainable paramters

At this point, you might be wondering:

*“We understand the self-attention mechanism, but where exactly do the trainable parameters come into play?”*

To clarify this, let’s first reiterate the original dimensions of the input word vectors before applying self-attention. *(Refer to the animation below for visualization where trainable parameters are.)*

### Understanding the Dimensions

In a standard setup, each word in a sentence is first **converted into an embedding** of a fixed dimension, say **d\_{model}**. If we have a sentence with ***N* words**, it is represented as:

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*1rIj6XD8yde1OuJu8o3jvA.png)

For example, let’s assume each word vector has a dimension of ***1 × 100***. That means:

- *V₂* (the word vector for the second word) is also *1 × 100*.
- The attention scores (*S₂₁, S₂₂, S₂₃*) and weights (*W₂₁, W₂₂, W₂₃*) are scalar values.
- The final contextualized word vector *Y₂* (after applying attention) remains *1 × 100*.

To make self-attention learnable, we introduce trainable weight matrices. Let’s break it down step by step.

### Transforming Input Vectors into Q, K, and V

Self-attention doesn’t directly use the original word vectors (*V*). Instead, each word vector is transformed into three different representations as discussed earlier:

**Query (Q)** — Represents the word we are focusing on.

**Key (K)** — Represents how much attention each word should receive.

**Value (V)** — Represents the actual word content used in attention computation.

`These transformations happen using learnable weight matrices.`

For *V₂* `(which acts as the query)`, we introduce a trainable matrix of shape 100 × 100, known as the Query matrix W\_Q. This ensures that the transformation doesn’t change the dimension of the vector.

Similarly, for `V₁, V₂, and V₃ (which act as keys)`, we introduce another trainable matrix of shape 100 × 100, called the Key matrix (W\_K). Again, this maintains the original dimensions.

Finally, when ***V₁, V₂, and V₃*** act as values, we apply a trainable Value matrix (W\_V) of size 100 × 100.

In summary, before calculating attention, each word vector V is transformed as follows:

*Q = V. W\_q,*

*K = V. Wₖ,*

*V = V. Wᵥ*

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*UghhITMkMhCWQuMY5jckQQ.gif)

Animation to Show Introduction of Trainable Weights

Here, W\_q, Wₖ, and Wᵥ are the learnable parameters that the model optimizes during training.

### Implementing Trainable Layers in Code

From a neural network perspective, we can implement these transformations as **linear layers (fully connected layers)**. If you’re implementing this in **PyTorch**,***as shown in the code snippet below*** you would define three separate `nn.Linear` layers for **Q, K, and V**.

```c
class MultiHeadAttentionBlock(nn.Module):

    def __init__(self, d_model: int, heads: int, dropout: float) -> None:
        super().__init__()
        self.d_model = d_model
        self.heads = heads
        assert d_model % heads == 0, "d_model is not divisible by heads"
        
        self.d_k = d_model // heads

        #defining weight parameter metrics
        self.w_q = nn.Linear(d_model, d_model) # query metrics
        self.w_k = nn.Linear(d_model, d_model) # weight metrics
        self.w_v = nn.Linear(d_model, d_model) # value metrics

        self.w_o = nn.Linear(d_model, d_model) # Ouput weight metrics, used after heads concatination
        self.dropout = nn.Dropout(dropout)
```

This setup allows the model to **learn** how to best transform the original word vectors into query, key, and value representations that improve attention calculations.

> Now, if you compare this with the original Transformer paper (*as shown in the image below*), you’ll recognize that this is exactly how **dot-product attention** works.

**However, we are not yet dealing with masked attention at this point. Also, we haven’t applied scaling yet, so it is not scaled dot-product attention yet.**

## Why Do We Scale the Attention Scores?

So far, we have computed the attention scores, but there’s one crucial step left — **scaling** the scores before applying softmax.

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*GN2y_unUxIcWCb9gmit75w.png)

You might be wondering:

*“We already have the attention scores, so why do we need to scale them?”*

Let’s break it down with intuition.

### Understanding the Scaling Factor

The attention score between a query ***Qᵢ*** and a key ***Kⱼ*** is computed using the dot product:

***Sᵢⱼ=Qᵢ ⋅ Kⱼ***

But here’s the issue:

- If the dimensionality of the word vectors (*dₖ*) is large, the raw dot product values can become very large.
- Large values fed into the softmax function can push it into its saturation region, where the gradients become extremely small (vanishing gradient problem).

To prevent this, we introduce a scaling factor by dividing the scores by *√dₖ* :

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*YuoB3wtSedTSm_G8hPgC_w.png)

where ***dₖ*** is the dimension of the key vectors.

### Intuition Behind Scaling

Imagine we have a **3D vector A** with all components as 2:

*A* = *(2,2,2)*

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*-P4fH7E_BUD6xHhiiLbimA.png)

The magnitude of this vector is:

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*15_VNW2SNiKkfYhGQ5IwUA.png)

Here, *dₖ* = 3

Now, if we divide by ***√dₖ*** , we get:

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*Mf5VM3CJD5nkgGVb0cjRIQ.png)

Notice that this gives us the average value of the vector components.

> That’s the c **ore idea behi** nd scaling! It helps **normalize the scores**, preventing them from exploding while maintaining their relative differences.

### Why Is Scaling Important for Large Dimensions?

In large models like **LLMs (GPT, BERT, etc.)**, the word embeddings typically have dimensions **512, 1024, or even larger**.

- Without scaling, the `dot product values would be huge.`
- `**Softmax would saturate**`, meaning the probabilities would be close to 0 or 1.
- When we take the gradient of softmax, the values would be too small, leading to vanishing gradients, making training unstable.

> By scaling the scores, we keep them in a reasonable range, ensuring that the gradient updates remain effective.

So, to summarize:

1. Trainable parameters come from the weight matrices **(*W\_Q, W\_K, W\_V*)** used to transform word vectors before self-attention.
2. These matrices allow the model to learn better attention representations.
3. Before applying softmax, we scale the attention scores to prevent instability in training.

This scaling step is crucial in large language models to maintain a stable gradient flow and ensure effective learning.

Now that we’ve covered scaling, let’s move on to the next step — **multi-head attention!**

## Multi-Head Attention: To get better understanding

Now that we understand self-attentionand how trainable parameters (Query, Key, and Value weight matrices) are introduced, let’s take this one step further:

### The Problem with Single Attention Head

In the self-attention mechanism, each word’s representation is updated based on its relation to other words in the sentence. However, a single attention function **focuses on only one pattern at a time**. This means:

- If the model attends to long-range dependencies, it might miss local interactions.
- If it captures word meaning, it might ignore syntactic roles (like subject-object relationships).

This is where multi-head attention comes in! Instead of using just one attention function, we use multiple parallel attention heads, allowing the model to capture different aspects of the input representation.

### Breaking It Down: How Multi-Head Attention Works

Let’s say our input vector embeddings have a dimension of *d\_model* = 512. Instead of passing them through a single set of Query, Key, and Value transformations, we create h independent attention heads (as mentioned in original paper, h = 8).

![](https://miro.medium.com/v2/resize:fit:3114/format:webp/1*2y7Q3bzSRUeV1TVsJh5TEg.jpeg)

Multi-Head Attention Explanation

Each head **learns different aspects** of the data by using its own separate Query, Key, and Value weight matrices:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*HHuE9rG3Ie4QHdInJpdiJg.png)

- Instead of keeping **Q, K, and V** dimensions as **d\_model**, we **split them into smaller subspaces**, making each head operate on lower-dimensional data.

For example, if `***d_model* = 512**` and we use `***h* = 8 heads**`, we assign each head a **reduced size of** `**d_head = d_model / h = 512 / 8 = 64**.`

So, each attention head independently computes its **Scaled Dot-Product Attention as below** :

> `*in below image the sub-script of K is ***i**** and not I.*`

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*BLfcH5bdth5fS78Hg6nMjQ.png)

Per head Attention Score

### Bringing It All Together: Concatenation & Final Projection

Once all **attention heads** compute their respective attention outputs (each of size **N × d\_head**), we **concatenate** them to restore the original dimensionality:

`*MultiHead(Q,K,V) *= *Concat(head₁ , head₂ , … , headₕ) . Wₒ*`

where *Wₒ* is another trainable projection matrix that re-maps the concatenated output back to d\_model dimensions.

### Why Use Multi-Head Attention?

1. **Captures Multiple -Representations:** Different heads focus on different relationships, like long-range dependencies, syntactic roles, and word meanings.
2. **Improves Expressiveness:** A single head might miss important interactions; multiple heads provide a richer understanding.
3. **Prevents Loss of Information:** Instead of compressing all attention into one vector, multi-head attention allows multiple perspectives before recombining them.
4. **Stabilizes Learning:** Each head works with lower-dimensional subspaces, preventing any single head from dominating learning.

## Conclusion

And that’s a wrap! I know this article got a bit long, but I wanted to break down the self-attention mechanism as simply and thoroughly as possible. Self-attention is the backbone of the Transformer architecture, which in turn has become the foundation of the modern AI revolution. Whether it’s LLMs, multi-modal models, or other cutting-edge applications, Transformers are everywhere — and understanding them starts with mastering self-attention.

By grasping the self-attention mechanism, you’ll be better equipped to analyze, optimize, and even build new algorithms on top of it. In this blog, I covered essential aspects like scaling and multi-head attention, focusing on the theoretical side. But don’t worry — soon, I’ll be publishing a hands-on blog where we’ll build a language model from scratch using decoder-only Transformers acrhitecture. Until then, if you’re eager for it’s practical implementation, I highly recommend checking out Andrej Karpathy’s *“* [***Let’s Reproduce GPT-2 (124M)***](https://www.youtube.com/watch?v=l8pRSuU81PU&list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ&index=10) *”* video.

### Refernces:

- **Bahdanau et al. (2014)**: “Neural Machine Translation by Jointly Learning to Align and Translate” introduced the attention mechanism in neural machine translation.
- **Luong et al. (2015)**: “Effective Approaches to Attention-based Neural Machine Translation” explored global and local attention mechanisms to enhance translation performance.
- **Vaswani et al.(2017):** Attention Is All You Need

*Thank you for taking the time to read and engage with this article. Your support in the form of following me and clapping on the article is highly valued and appreciated. If you have any queries or doubts about the content of this article, please do not hesitate to reach out to me via email at* ***manindersingh120996@gmail.com****. You can also connect with me on 🔗* [*LinkedIn*](https://www.linkedin.com/in/manindersingh120996)*.*