---
title: "The Complete Guide: How to Become an ML Engineer"
source: "https://x.com/ArmanHezarkhani/status/2013608521900683765"
author:
  - "[[@ArmanHezarkhani]]"
published: 2026-01-20
created: 2026-04-06
description: "This is not engagement bait. If you do everything in this guide, you will be able to train large language models on your own.The key is to g..."
tags:
  - "clippings"
---
This is not engagement bait. If you do everything in this guide, you will be able to train large language models on your own.

The key is to get through every step of this guide, step by step, following everything I prescribe. If you do that, you'll be an ML engineer.

I've taught millions of people how to code (yes, really). Here's everything I've learned about the optimal learning path for ML/AI specifically. If it seems simple, just commit to getting it done.

## Stop Learning Like It's Netflix

The biggest mistake people make with educational videos is treating them like entertainment. Watch passively, maybe take some notes, move on. A week later, everything's gone.

That's not how you learn technical material.

You need two passes through every video. This feels slow. It's not. It's the only thing that actually works.

**First pass: Just watch.** Start to finish. Don't take notes. Don't pause to code along. Don't try to understand every detail. Your goal is to get the shape of the material in your head. What are the main concepts? How do they connect? You're building a mental scaffold that the details will hang on later.

**Second pass: Active learning.** Now watch again—but differently.

Open a notebook. Open a Jupyter notebook or Python file. Have both ready.

This time:

- **Pause constantly.** Every time something important happens, stop.
- **Take full notes.** Write concepts in your own words. Don't copy—translate.
- **Type out all the code yourself.** Don't copy-paste. Type every character. This forces your brain to process it.
- **Break stuff.** After you get code working, change things. What happens if you modify this parameter? What if you remove this line?
- **Try stuff.** Have a random idea? Try it. See what happens.
- **Jot down interesting observations.** Notice something unexpected? Write it down.

This second pass will take 2-3x longer than the video itself. That's the point. You're not watching—you're learning.

The people who become great ML engineers aren't smarter than you. They just put in this kind of deliberate practice while everyone else watches videos on 2x speed.

## What You're Actually Learning For

Before you start, understand what an ML engineer actually does.

An ML engineer is not a data scientist. Data scientists analyze data and build models to answer business questions. ML engineers build the systems that make those models work in production—at scale, reliably, efficiently.

An ML engineer is not a researcher. Researchers push the boundaries of what's possible. ML engineers take what researchers discover and make it actually useful.

**What ML engineers actually do:**

- Train and fine-tune models
- Build data pipelines that feed models
- Deploy models to production systems
- Optimize models for speed and cost
- Monitor model performance and handle drift
- Integrate AI capabilities into applications

**What you need to know:**

- Programming (Python, primarily)
- Linear algebra and calculus (enough to understand what's happening)
- How neural networks work—not just conceptually, but mechanically
- The transformer architecture that powers everything modern
- How to actually implement these things in code

The last point is critical. You can't become an ML engineer by watching videos passively. You have to build things. Break things. Understand things at the code level.

# Phase 1: Build Intuition with 3Blue1Brown

Grant Sanderson is the best math educator on the internet. His neural networks series takes complex concepts and makes them visually intuitive.

Start here. Even if you have some ML background, start here. The visual intuition you'll build is invaluable.

**Time investment: ~10-15 hours total**

## Chapter 1: But what is a Neural Network?

**Link:** [https://www.youtube.com/watch?v=aircAruvnKk](https://www.youtube.com/watch?v=aircAruvnKk)

The foundation. This video answers the most basic question: what actually is a neural network?

You'll learn about neurons, layers, weights, biases, and activation functions. More importantly, you'll see them—the animations make abstract concepts concrete.

Don't skip this even if you think you know what a neural network is. Grant's explanation will give you a cleaner mental model than whatever you currently have.

## Chapter 2: Gradient descent, how neural networks learn

**Link:** [https://www.youtube.com/watch?v=IHZwWFHWa-w](https://www.youtube.com/watch?v=IHZwWFHWa-w)

How does a network actually learn?

This video explains gradient descent—the core algorithm that powers all of deep learning. You'll see how a network adjusts its weights to get better at its task, step by step.

The cost function visualization here is particularly valuable. When you understand why we're minimizing a cost function and how gradient descent does it, everything else in ML makes more sense.

## Chapter 3: What is backpropagation really doing?

**Link:** [https://www.youtube.com/watch?v=Ilg3gGewQ5U](https://www.youtube.com/watch?v=Ilg3gGewQ5U)

Backpropagation is the algorithm that makes neural network training practical. This video explains the intuition—what's actually happening when a network learns.

Most courses throw calculus at you immediately. Grant builds the intuition first. You'll understand why backprop works before you see the math.

## Chapter 4: Backpropagation calculus

**Link:** [https://www.youtube.com/watch?v=tIeHLnjs5U8](https://www.youtube.com/watch?v=tIeHLnjs5U8)

Now the math. This video walks through the calculus behind backpropagation—the chain rule in action.

This is where some people get scared off. Don't be. You don't need to be a calculus expert. You just need to follow the logic of how gradients flow backward through the network.

If the math feels hard, watch this one multiple times. It's worth the effort. Understanding backprop at the calculus level separates people who use ML from people who understand it.

## Chapter 5: Large Language Models explained briefly

**Link:** [https://www.youtube.com/watch?v=LPZh9BOjkQs](https://www.youtube.com/watch?v=LPZh9BOjkQs)

A bridge to modern AI. This video provides a lightweight intro to LLMs—what they are, how they relate to the neural networks you just learned about.

Think of this as a preview. You'll go much deeper with Karpathy later. For now, you're just connecting your foundational knowledge to the systems that power ChatGPT and Claude.

## Chapter 6: Transformers, the tech behind LLMs

**Link:** [https://www.youtube.com/watch?v=wjZofJX0v4M](https://www.youtube.com/watch?v=wjZofJX0v4M)

The transformer architecture is the breakthrough that made modern AI possible. This video gives you a visual introduction to how transformers work.

Pay close attention to the architecture diagrams. You're building intuition you'll need when you implement these things in code later.

## Chapter 7: Attention in transformers, step-by-step

**Link:** [https://www.youtube.com/watch?v=eMlx5fFNoYc](https://www.youtube.com/watch?v=eMlx5fFNoYc)

Attention is the key mechanism inside transformers. This video breaks it down step by step.

Queries, keys, values—these terms get thrown around constantly in ML. After this video, you'll actually understand what they mean and why they matter.

## Chapter 8: How might LLMs store facts

**Link:** [https://www.youtube.com/watch?v=9-Jl0dxWQs8](https://www.youtube.com/watch?v=9-Jl0dxWQs8)

This video unpacks the multilayer perceptrons in a transformer—the parts of the network that seem to store factual knowledge.

It's a fascinating look at what might be happening inside these models. Not just how they work mechanically, but what they might actually be doing.

## Bonus: How do AI images and videos actually work?

**Link:** [https://www.youtube.com/watch?v=iv-5mZ\_9CPY](https://www.youtube.com/watch?v=iv-5mZ_9CPY)

A guest video covering diffusion models—the tech behind image generators like DALL-E, Midjourney, and Stable Diffusion.

This expands your understanding beyond language models. Modern ML engineering often involves multiple modalities.

# Phase 2: Build Implementation Skills with Karpathy

If 3Blue1Brown gives you the intuition, Andrej Karpathy gives you the implementation.

Karpathy was the founding member of OpenAI and former Senior Director of AI at Tesla. He's one of the most influential ML educators alive. This course is how you learn to actually build things.

**Prerequisites:** You should be comfortable with Python. You need basic math—derivatives, gaussian distributions, that kind of thing. If you've finished the 3Blue1Brown series, you're ready.

**Time investment: ~30-40 hours total**

## Video 1: Building micrograd

**Link:** [https://youtu.be/VMj-3S1tku0](https://youtu.be/VMj-3S1tku0) **Duration:** 2 hours 25 minutes

This is where it gets real.

Karpathy builds an entire automatic differentiation engine from scratch. From nothing to a working neural network that can learn—in pure Python, no libraries.

This video is legendary in the ML community. By the end, you'll understand backpropagation at a level most ML practitioners never reach. You'll have built it yourself.

Take your time with this one. Type every line of code. Build micrograd yourself. This is the foundation everything else builds on.

## Video 2: Building makemore

**Link:** [https://youtu.be/PaCmpygFfXo](https://youtu.be/PaCmpygFfXo) **Duration:** 1 hour 57 minutes

Now you build a character-level language model. Given some text, the model learns to generate more text like it.

This introduces you to language modeling—the core task behind LLMs. You'll implement it from scratch, understanding every piece.

By the end, you'll have a model that can generate fake names, fake words, fake whatever you train it on. More importantly, you'll understand how it does it.

## Video 3: Building makemore Part 2: MLP

**Link:** [https://youtu.be/TCH\_1BHY58I](https://youtu.be/TCH_1BHY58I) **Duration:** 1 hour 15 minutes

You rebuild makemore using a multi-layer perceptron (MLP). This is the architecture described in a famous Bengio et al. paper.

Now you're implementing ideas from actual research papers. This is what real ML engineering looks like—reading papers and implementing them.

## Video 4: Building makemore Part 3: Activations & Gradients, BatchNorm

**Link:** [https://youtu.be/P6sfmUTpUmc](https://youtu.be/P6sfmUTpUmc) **Duration:** 1 hour 55 minutes

This video dives into the internals of neural network training. Activations, gradients, why things go wrong, and how to fix them.

Batch normalization is one of those techniques that makes training actually work. You'll understand why it exists and how to implement it.

## Video 5: Building makemore Part 4: Becoming a Backprop Ninja

**Link:** [https://youtu.be/q8SA3rM6ckI](https://youtu.be/q8SA3rM6ckI) **Duration:** 1 hour 55 minutes

This is where Karpathy turns you into someone who truly understands backpropagation.

You'll implement backprop manually through complex operations. By the end, you'll be able to derive gradients through anything. This skill separates ML engineers from ML users.

## Video 6: Building makemore Part 5: Building a WaveNet

**Link:** [https://youtu.be/t3YJ5hKiMQ0](https://youtu.be/t3YJ5hKiMQ0) **Duration:** 56 minutes

You implement a WaveNet-style architecture with dilated convolutions. This shows how architectural innovations solve specific problems.

Shorter video, but important concepts about how modern architectures handle sequential data.

## Video 7: Let's build GPT

**Link:** [https://www.youtube.com/watch?v=kCc8FmEb1nY](https://www.youtube.com/watch?v=kCc8FmEb1nY) **Duration:** 1 hour 56 minutes

The crown jewel. You build GPT—the architecture behind ChatGPT—from scratch.

This video walks through the entire transformer implementation. Attention, positional encodings, the whole thing. By the end, you'll have a working GPT that you built yourself.

This is the video that made thousands of people actually understand modern AI. Don't just watch it—build it.

## Video 8: Let's build the GPT Tokenizer

**Link:** [https://youtu.be/zduSFxRajkE](https://youtu.be/zduSFxRajkE) **Duration:** 2 hours 13 minutes

Tokenization is how text becomes numbers that neural networks can process. This video builds the tokenizer used in the GPT series.

Most people ignore tokenization. That's a mistake. Understanding how text becomes tokens reveals a lot about how LLMs actually work—and why they sometimes behave strangely.

# Phase 3: Deepen Context with Bonus Videos

These videos aren't part of the main course, but they're valuable for context and broader understanding.

**Time investment: ~5 hours total**

## Intro to Large Language Models

**Link:** [https://www.youtube.com/watch?v=zjkBMFhNj\_g](https://www.youtube.com/watch?v=zjkBMFhNj_g) **Duration:** 1 hour

A general-audience introduction to LLMs. Great if you want a high-level overview before diving into the technical content, or as a way to explain what you're learning to others.

Covers how LLMs work, future directions, and security considerations.

## Deep Dive into LLMs like ChatGPT

**Link:** [https://www.youtube.com/watch?v=7xTGNNLPyMI](https://www.youtube.com/watch?v=7xTGNNLPyMI) **Duration:** 3 hours 31 minutes

Karpathy's most comprehensive overview. Covers the entire training stack—pretraining, supervised fine-tuning, reinforcement learning.

Also covers "LLM psychology"—how to think about hallucinations, tool use, what models know about themselves. Essential context for anyone who will work with these systems.

# The Complete Roadmap

Here's your path from zero to ML engineer:

**Phase 1: Build Intuition (3Blue1Brown)**

- Watch all videos in order
- First pass: just watch
- Second pass: notes and active engagement
- Time: ~10-15 hours

**Phase 2: Build Implementation Skills (Karpathy Zero to Hero)**

- Work through videos 1-8 in order
- Type all code yourself
- Break things, try things, edit things
- Time: ~30-40 hours

**Phase 3: Deepen Context (Bonus Videos)**

- Watch the general audience videos
- Fill in gaps and build broader perspective
- Time: ~5 hours

**Total time: ~50 hours of focused study.**

That's it. Fifty hours and you'll understand modern AI at a level most people never reach. You'll have built neural networks, language models, and GPT from scratch.

# TL;DR

**The path is free and on YouTube.** 3Blue1Brown for intuition, Karpathy for implementation. That's the curriculum.

**How you watch matters more than what you watch.** First pass: just watch. Second pass: notebook open, Jupyter open, type everything, break things, try things.

**3Blue1Brown builds visual intuition.** Neural networks, gradient descent, backprop, transformers, attention. ~10-15 hours.

**Karpathy builds implementation skills.** You'll build micrograd, makemore, and GPT from scratch. Type every line of code yourself. ~30-40 hours.

**You need both understanding and skills.** Intuition without implementation is useless. Implementation without intuition is fragile.

**This takes ~50 hours of focused work.** Not passive watching—active learning. That's the investment that actually pays off.

The people who become great ML engineers aren't waiting for the perfect course or the right bootcamp. They're learning from the best resources available—which happen to be free—and putting in the deliberate practice.

**Start watching. Start building.**