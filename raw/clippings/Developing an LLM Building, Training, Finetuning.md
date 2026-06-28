---
title: "Developing an LLM: Building, Training, Finetuning"
source: "https://www.youtube.com/watch?v=kPGTx4wcm_w"
author:
  - "[[Sebastian Raschka]]"
published: 2024-06-06
created: 2026-04-12
description: "REFERENCES:1. Build an LLM from Scratch book: https://amzn.to/4fqvn0D2. Build an LLM from Scratch repo: https://github.com/rasbt/LLMs-from-scratch3. Slides: https://sebastianraschka.com/pdf/slides/"
tags:
  - "clippings"
---
![](https://www.youtube.com/watch?v=kPGTx4wcm_w)

REFERENCES:  
1\. Build an LLM from Scratch book: https://amzn.to/4fqvn0D  
2\. Build an LLM from Scratch repo: https://github.com/rasbt/LLMs-from-scratch  
3\. Slides: https://sebastianraschka.com/pdf/slides/2024-build-llms.pdf  
4\. LitGPT: https://github.com/Lightning-AI/litgpt  
5\. TinyLlama pretraining: https://lightning.ai/lightning-ai/studios/pretrain-llms-tinyllama-1-1b  
  
DESCRIPTION:  
This video provides an overview of the three stages of developing an LLM: Building, Training, and Finetuning. The focus is on explaining how LLMs work by describing how each step works.  
  
\---  
  
To support this channel, please consider purchasing a copy of my books: https://sebastianraschka.com/books/  
  
\---  
  
https://twitter.com/rasbt  
https://linkedin.com/in/sebastianraschka/  
https://magazine.sebastianraschka.com  
  
\---  
  
OUTLINE:  
  
00:00 – Using LLMs  
02:50 – The stages of developing an LLM  
05:26 – The dataset  
10:15 – Generating multi-word outputs  
12:30 – Tokenization  
15:35 – Pretraining datasets  
21:53 – LLM architecture  
27:20 – Pretraining  
35:21 – Classification finetuning  
39:48 – Instruction finetuning  
43:06 – Preference finetuning  
46:04 – Evaluating LLMs  
53:59 – Pretraining & finetuning rules of thumb

## Transcript

### Using LLMs

**0:00** · Yeah, hi, everyone. So today I want to talk about developing an LLM, a large language model. And in particular, I want to talk about the three stages, building, training and fine tuning large language models. So but before we begin with the building aspect of large language models, I wanted to briefly go over the different use cases or the different ways we are using large language models. So the maybe most popular way to use large language models these days is via a public or proprietary service, like a public API or proprietary API. So for example, ChatGPT, or Perplexity AI, Gemini and others. So we would basically go to a website, ask, or give the LLM an instruction or ask it a question. And then it returns the answer. So this would be one way of using a large language model.

**1:01** · The other one is Yeah, nowadays also very popular thanks to open source and open weights. So that's running a custom large language model locally. So here's an example running a llama three model 8 billion Llama 3 model. And yeah, I can also similarly give it my query in my terminal here and interact with the LLM let's say locally. And here I'm using a particular tool called LitGPT that I help developing. So another way then is also deploying a custom large language model, for example, deploying it on an external server or web service. And then we can also use the LLM by an API. And this is especially useful or interesting if we are developing products. So going back one slide. So here, it's really more like for me as a customer, I can, or as a user, I can run my own LM and use it. And this one is, for example, an option where I can still run my LLM locally on server. But the difference is that we have an API endpoint that we can then use, for example, in an application that could be user interface, like ChatGPT, like the UI, but it could also be an iPhone app or something like that. So I would say, yeah, these are the three common ways of how we are using LLMs, like the typical ways to interact with them.

**2:30** · They are all different use cases, and they also have different trade offs. Personally, I use all three of them. So for different, you know, for different tasks, or for different goals, I use different approaches, and there is no right or wrong. And there's no better or worse, they all have different kinds of trade offs. So, but today, this talk is not about the different trade offs of these usages, I wanted to pull the curtain back a bit and talk about what goes into developing LLMs that we can then run, like I've shown you before. So what goes into creating that LLM in the first place, in particular, I want to talk about these different stages of developing an LLM. So this involves building the LLM itself. So here, we have to prepare the data, sampling the data set, and so forth, we have to do some coding, implement this attention mechanism that is at the heart of the LLM, it's essentially the motor, if you will, of the LLM. And then of course, also coding the whole architecture around it. So if the attention mechanism is, let's say the motor of a car, that architecture would be basically everything surrounding that motor, like connecting the wheels, putting driver seats in, and a steering wheel, and everything else.

### The stages of developing an LLM

**3:53** · The second stage, then is the pre training stage. So this would be essentially taking a large language model, a large language model architecture, and then training it on a data set. For that, we have to implement the training loop, the model evaluation. And usually, we also want a mechanism to save and load pretrained weights so that we can use the large language model later, because usually this stage is what forms a so called foundation model. So that's usually not our end product. It's like an intermediate, I would say, product in this pipeline. But in general, it's more like the foundation or the base model that we use then for finetuning. And so finetuning, yeah, that can be different things. So we could, for example, finetune a model to do classification, you know, like text categorization, identifying spam email, and these types of things. But we can also get train a personal assistant, a chatbot. For that, we can use an instruction data set, for example. So, by the way, all the figures I'm showing you are from my book, Build A Large Language Model from Scratch. So I made all these figures for my book. And I'm just reusing them here (not all of them), but many are from the book. And in the book is also more code if you actually want to build it because this talk is only conceptual. So here I'm going over the concepts. And if you're interested in coding something like this yourself, you have more details in the book. And also I have a GitHub repository with all the code examples. So starting with stage 1, the building here ...

### The dataset

**5:29** · So here we will be putting together the LLM architecture itself. But even taking a step back before we implement the architecture, we will take a look at the data set, how the data set looks like, or how a data set looks like, and then how we feed that data set into the large language model. And this is actually, in my opinion, a good way of understanding how an LLM works, because understanding how an LLM works kind of requires to understand what it works with, what does the data set look like.

**6:02** · So if we understand how we feed the data into the LLM, we are already closer to understanding how the mechanism, the LLM architecture works and so forth. So, yeah, this is the reason why at the very left here, we are starting with the data set preparation and sampling, explaining it before we actually do the pretraining, because I do think it helps understanding a bit how an LLM works.

**6:29** · So, yeah, an LLM is essentially, you can think of it as a deep neural network if you have done deep learning before.

**6:37** · So especially I think if you're watching this video, you have maybe seen some of my other videos on YouTube.

**6:43** · So you probably have some background in machine learning and deep learning.

**6:47** · So for now, I would say, the simplest way to think of a large language model is really to think of it as a large, deep neural network.

**6:57** · And this deep neural network is a model that is trained to predict the next word in the text.

**7:04** · So that's the first stage.

**7:05** · When we do the pretraining, we train the model to predict just the next word in a sentence or in a text.

**7:13** · And yeah, we call that also sometimes the next-word prediction task, but, essentially it's a next-"token" prediction task.

**7:20** · And I will also explain in a bit what the token is.

**7:24** · So just to show you what that looks like.

**7:26** · So if we have an example text here at the top, the example text is LLMs learn to predict one word at a time.

**7:34** · So I want to train, let's say the model on this text, of course, the real world dataset is much, much larger.

**7:40** · It's billions of words, but just, you know, to give an example that fits into this slide.

**7:45** · So on the left hand side, if we have a sentence like that, we take to start with the left word, let's say LLMs here.

**7:53** · That is what the LLM receives as an input.

**7:57** · Then the learn is the target that it should predict.

**8:00** · So that's the next word and everything right from the target here on the right hand side is for now hidden from the LLM.

**8:07** · So we are just feeding it LLMs, the word LLMs, and then, it's supposed to predict the next word learn in this case.

**8:15** · So I'm here, let's say our two training input examples.

**8:19** · So the first sample is "LLMs", the model, generates or supposed to generate "learn".

**8:25** · The second sample, "LLMs learn" and then the next word it should predict is "to".

**8:31** · And then we continue on to construct the data set such that we give the LLM learning tasks where one word is missing and it's supposed to generate this next word.

**8:42** · We'll, I will explain later, a bit more, let's say how, that works.

**8:48** · So this is how the pretraining or let's say the training function works, I will say a few more words about that. But in general, that's how we would prepare a data set for pretraining.

**8:59** · Now in practice, this would be quite inefficient to feed it just one sentence or text at a time.

**9:07** · So in practice, what we do is we do a batching like we do in deep learning in general.

**9:12** · So what that means is we are putting multiple training inputs together into a batch and usually batches have to have the same length because they are implemented as tensors.

**9:24** · So where we can think of it almost like, yeah, as a matrix.

**9:27** · And, so we have to have the same number of elements in the columns.

**9:32** · So usually, we prepare the data set like that, where we take, fixed size inputs, sliding it over the text here to create such a batch.

**9:42** · And we would do that for the whole data set then.

**9:46** · Of course, I'm only showing you, what is one, two, three, four, um, four words in one row.

**9:54** · But in reality, these are much larger.

**9:56** · Yeah. So usually we are working with input lengths of at least, I would say, 256 for a very small model, 1024 or even larger for pretraining.

**10:07** · So we usually, yeah, give it bigger inputs.

**10:10** · But again, this is a small text example just to make it fit onto this slide here.

### Generating multi-word outputs

**10:16** · So the question now is if we, if we just predict one word at a time, so if we train the LLM so that it can only predict the next word.

**10:25** · How can an LLM actually then generate a multi-word output?

**10:29** · So for example, in the case, if you used ChatGPT before, it can generate this whole output all at once, how does that work?

**10:40** · So this is usually, still a one word prediction task per iteration.

**10:45** · So here, for example, if I have an input and that is called the sentence, let's say the text is "this" and feed it to the LLM, the output here.

**10:56** · Here would be, "this is", so it's still, generating only the next word, but what we do then is we pass this, output here.

**11:05** · So I hope you can see that you can pass this output here back into the LLM.

**11:10** · And so the context here is now one word more than before it passes again through the LLM and now it's, "this is an".

**11:18** · So if we added another word and then again, we take this output, feed it back to the LLM.

**11:25** · And then, we have one word more and we keep on doing this until, either we generate a so-called end of text token, which is a special token that will stop the generation process or we reach a, let's say, system or user-specified number of tokens.

**11:44** · And, if you next time, if you use ChatGPT, you have to maybe, if you let's say pay attention if you put in some input texts, some longer input that requires a longer answer, you will see it's also generating one word at a time in this output.

**11:59** · It's like this visual cue almost where it doesn't generate all the output all at once.

**12:05** · You don't see the block of text appearing all at once.

**12:08** · It's really, showing you also this, um, word by word generation, which is, I feel like a small, gimmick in the UI, but it also kind of highlights in a way how LLMs generate texts.

**12:21** · Um, yeah.

**12:22** · So, this is how we get from the let's say next word prediction task to actually generating, longer outputs.

### Tokenization

**12:31** · So there's one more thing I mentioned earlier, actually we are not generating one word at a time.

**12:36** · It's called a "token" actually.

**12:39** · So there's a small distinction between words and tokens.

**12:42** · So if we have some input text here, what happens internally is that this input text gets tokenized.

**12:49** · So it's basically, in this very simple example, tokenized based on white spaces, but that's just a very simple example.

**12:57** · And, usually it's a bit more complicated, but the general concept is that we break down the sentence into individual word tokens or punctuation in this case.

**13:06** · So we have from this input text, one, two, three, four, five tokens.

**13:11** · And from that, we then, get to token IDs.

**13:14** · So, this is, I'm not showing in this presentation because that would be maybe more like a three hour presentation rather than a 45 minute presentation.

**13:24** · Okay.

**13:25** · But so there's usually a vocabulary that we built based on all the unique words in the training data set and based on that vocabulary, we assign them these token indices.

**13:38** · So the words you can see with, smaller, letters, sorry, with letters that come early in the alphabet, have smaller numbers and this is a larger number you show, you know, like if it's alphabetically, punctuation, maybe, and numbers come first. Then these smaller words or tokens with "a", at the beginning, and then, alphabetically, you can see they get larger and there is actually, also a more sophisticated process of play.

**14:09** · I mean, depends on what LLM (/tokenizer) you are working with, but for example, GPT originally, I think they still do use a modified version of that.

**14:17** · It's called a BPE tokenizer.

**14:19** · I think it stands for byte pair encoding, if I recall correctly.

**14:24** · And there are ...

**14:24** · there are variations of that, like SentencePiece for Llama.

**14:28** · And so these tokenizers can also deal with unknown words.

**14:32** · So if you have an unknown word, so like some word or two words I made up here, they would then be sub-tokenized.

**14:39** · So you can see, it breaks it down like this.

**14:42** · So what I'm trying to say is even if your words didn't appear in the training set, when you build this BPE tokenizer, or if you use an existing, PE tokenizer that has not been seeing such a word, it would still be able to give you tokens.

**14:59** · It's just giving you more tokens now.

**15:00** · So it's not one token per word.

**15:03** · It's like, for this word, it's like one, two, three, four, four tokens because it doesn't recognize the word.

**15:09** · So it's breaking it down into individual letters here in this case.

**15:12** · And this is why to some extent, LLMs also work with unknown words they wouldn't crash or something, but it's, yeah, it's just inefficient basically.

**15:22** · So you want to.

**15:25** · try to represent all the, uh, words in the vocabulary if you can, but of course, if a user comes up with a new word or something, it shouldn't fail or crash.

### Pretraining datasets

**15:35** · Okay.

**15:36** · So I talked about simple data sets in reality, there are also data sets that are used for training LLMs are much larger than the small snippets I've shown you.

**15:46** · So back then, for example, when, GPT-3 was trained, it was trained on almost 5 billion, 500 billion (so it's half a trillion) tokens.

**15:57** · This is, back in 2020, a long time ago.

**16:00** · And but, uh, what's nice about this is also back then researchers still showed, roughly showed, what they used for training.

**16:10** · So they shared a bit of the details that went into training that model.

**16:15** · So for example, they talk a bit about, in the paper, what these data sets are, for example, Wikipedia data sets and book data sets.

**16:23** · Website, crawl data set and so forth.

**16:27** · And nowadays ... it's less common nowadays.

**16:30** · It's really they maybe tell you how big the data set was, but they don't share any details anymore.

**16:37** · So, but another example from, back then, I think this should actually be 2023.

**16:44** · I have to correct this, what's Lama one by Meta AI and here, they trained.

**16:49** · So my main point was essentially training sets are getting larger.

**16:53** · So we are going from 500 billion to 1.4 trillion.

**16:57** · It's, three times larger now, even larger when we go to Llama 2, so it's 2 trillion and then Llama 3, it's 15 trillion, but going back a step: So here we can still see what went into that data.

**17:11** · So we have GitHub now, arXiv papers, StackOverflow and StackExchange data and so forth.

**17:20** · New models, they don't actually reveal that information anymore.

**17:23** · It's just says a new mix of data from publicly available sources.

**17:28** · And for Lama 3, it's 15 trillion tokens that were all collected from publicly available sources.

**17:35** · It's a bit unfortunate if you, you know, as a researcher, I want to know a bit more how the data set looked like, for example, if you are trying to put down or together your own data set.

**17:47** · But I think this is really because some companies have been sued by training on data that was protected.

**17:56** · So basically we actually shouldn't go out and just train LLMs on publicly available data because publicly available doesn't mean we are supposed or allowed to use that data.

**18:08** · And so I guess by not saying what the data set is here, researchers try, or companies try to avoid lawsuits.

**18:17** · So yeah, also I should say in my book, um, I'm only training, the LLM on example, data in the public domain where this is from data that is not copyrighted so i'm also making sure of that because I, yeah, I think we should respect that if data is let's say not designated for training we probably shouldn't use that. Anyways so here I just wanted to show you or highlight the sizes of the different data sets that have been used to train LLMs. So the trend goes towards more data according to the scaling laws for a certain size we still haven't saturated the performance of LLMs. So with more data we can still squeeze out more performance.

**19:02** · The only recent paper I would say that I'm aware of or a model that I'm aware of that went into a bit of a different trend is the Phi 3 model by Meta sorry by Microsoft I mean so the Phi model by Microsoft.

**19:20** · They focused more on developing smaller models with smaller amounts of data. So they argue here actually even using less data that would be considered optimal would actually be beneficial to the LLM because you leave some let's say capacity for learning certain behaviors or reasoning for example. So here for example they say they don't ex they don't include the result of a game in premier league in a particular day because this is, I mean, this is correct information but it's not necessary that useful to memorize... you know like i wouldn't say it's trivial for premier league fans no offense here, I watch also sometimes premier league games: Liverpool. So I'm a Liverpool fan in particular but in general I would say depends on what you want to build here.

**20:19** · So unless you are trying to build a sports knowledge base or something like that it's maybe not necessary to feed all that data about all the games into the LLM. Because then you trade it off with other things or qualities so here they argue on that they leave more capacity for reasoning by not training the model on too much data for example. I mean, this is a hypothesis yeah a valid argument, I would say but of course also as others have shown more data can be better.

**20:56** · So it's, you know, it's something I think that we will see trickling out in the upcoming months or years when we see some other or additional architectures on doing some investigation here.

**21:09** · Because these are both very recent papers. Or, Lama 3 is not even published as a paper it's just released so we don't have really that much information about these yet.

**21:19** · Phi 3 just came out a few weeks ago so in that case we need to really see more research to say whether this is an actual thing here with the capacity. Okay, moving on though. So we talked about the data we understand a bit now how an LLM receives data, that it learns to predict the next word. But what goes into developing an LLM that can read this data? What is let's say the architecture? What do the architectures look like here? So let's talk about the architecture and then I will briefly revisit the pretraining and then we will talk about model evaluation and the finetuning stages. So, because I fear this talk might be a very long talk that might go many many hours I'm not going into too much detail of these individual components but I'm just showing you how or how the original and GPT-2 and 3 models look like. So this is the basic architecture that was used to develop the GPT models. We don't know exactly how GPT-4 looks like. So there's no paper about that but for the first three GPT models it's this type of architecture here. And there are certain components (I will maybe say something about that later) that are not used anymore. But in in general it's this, the same cookie cutter template that is also used for other LLMs.

### LLM architecture

**22:51** · So in particular, there's this masked multi-head attention module.

**22:55** · There are feed forward layers.

**22:57** · It's essentially two linear layers usually with a nonlinear activation.

**23:02** · The SiLU or SiLU activation, they have, it depends also how you structure it, but it has, it can have three linear layers depending on how you write the code.

**23:13** · Yeah, positional embedding layer.

**23:14** · It's usually for the input token embedding layer.

**23:17** · And yeah, this is a layer norm here.

**23:20** · Some architectures use RMS norm, but this is the overall architecture.

**23:23** · What's interesting is, here in blue, that is the so-called transformer block.

**23:29** · And this is an element that is repeated a number of times.

**23:33** · And that really depends on, on the size of the LLM.

**23:36** · But usually I would say you repeat that at least 12 to 32, 64 times, depending on the size of the LLM.

**23:44** · You actually have some numbers.

**23:46** · So, for the small, so here, maybe to back up a bit.

**23:50** · So here are different sizes of the GPT two model, from 124 million parameters to 1.5 billion or 1,500 million.

**24:00** · And the difference between these architectures is really, I would say minor.

**24:05** · It's really just the number of times you repeat this transformer block from 12 to 48.

**24:11** · And, also the number of heads in the multi head attention mechanism.

**24:14** · It's essentially, if you are familiar ...

**24:17** · I should maybe make a lecture on that too ... but if you're familiar with, convolution networks, if you think about the channels in a convolution, the convolution layer, you can think of the.

**24:29** · heads in multi-head attention as an equivalent.

**24:31** · So it's basically stacking, like stacking, channels and a convolution network here.

**24:36** · You're stacking these multi-head attention heads.

**24:40** · And really the difference between the small model and the large model is just the number of times you'll repeat this, like how many, how deep your stack is, but it's the same element.

**24:51** · So, the key idea here is really that we are reusing elements and we are just, you know, duplicating these elements to make the models larger.

**24:59** · Another small difference here is the embedding dimension.

**25:01** · For example, the smallest one has 768 and the larger one has, um, 1,600.

**25:07** · I think nowadays it's also common to go 4,000 to 8,000, for example.

**25:13** · So, just to take an example from a Llama.

**25:17** · So the Meta 2, uh, sorry, the Meta AI Llama 2 models, the 7 billion version ...

**25:21** · so what they've done, what they've done here is they've replaced layer norm with RMSNorm. And RMSNorm, root mean square norm, is basically what most, I would say most modern architectures use.

**25:35** · It's basically a normalization layer, similar, if you're familiar with batch norm, it's kind of like batch norm, but it works better for multi GPU training essentially. Because you can have, you don't have to gather over the batch size basically.

**25:51** · So it's batch-size-independent is what I'm trying to say.

**25:55** · Yeah, so you have the SiLU instead of, um, GELU activation here. You repeat it 32 times in the case of 7B model.

**26:03** · You don't have dropout and yeah, for the embedding layers, usually we use, for the, for the positional embedding, we use a RoPE.

**26:13** · I think it stands for rotational positional embeddings.

**26:16** · So ...

**26:16** · the first GPT model has absolute, an absolute position embedding and the yeah newer models they use a relative positional embedding and the the size is a bit bigger: Before we had 1028 tokens.

**26:32** · Now we have 4,000 it's four times, yeah, three times as large, basically. A bit more than three times, but yeah.

**26:40** · Yeah, and this is essentially, I would say the main difference. The takeaway.

**26:46** · here's really that most LLMs are still very similar to each other.

**26:50** · They are very small, I would say changes, in some LLMs like these. And that's also why in LitGPT, for example, we, yeah, we implemented a lot of LLMs based on the same base architecture.

**27:03** · Because really these are relatively small changes.

**27:06** · It's not really, um, I would say reinventing the wheel and it works well.

**27:10** · So people still, yeah ...

**27:12** · keep building with that architecture here.

**27:14** · The, it all goes back to the original GPT architecture basically.

### Pretraining

**27:21** · So now that we have familiar with the architecture, let's briefly return to the pretraining.

**27:27** · So the pretraining is essentially what creates the so-called foundation model, which is then used for finetuning later.

**27:35** · So I'm not going over the training loop because, yeah, it would look pretty technical if you are not familiar with training loops and it looked, it would look very boring.

**27:46** · If you are familiar with training loops, because it's really just like a standard deep learning training loop.

**27:53** · There's really nothing different from training I would say convolutional networks multi-layer perceptrons ... you use the same Adam optimizer, same learning rate scheduler like, 1-cycle cosine schedule and so forth use the same cross entropy loss.

**28:12** · So it's all the sameb basically that we would use when training convolution networks, recurrent neural networks, (recurrent neural networks are maybe a bit different), but convolutional networks, multi-layer perceptrons and so forth.

**28:24** · And, I would say the, the only difference is really that we do that on a larger scale on multiple GPUs.

**28:30** · And here the tricky part is more like, the hardware access and, and that type of stuff.

**28:40** · What, what do the labels look like?

**28:42** · We talked about this before already.

**28:44** · So the target, so when you train, for example, in classic deep learning or convolution network, it's usually for some prediction task, for example, um, let's say, uh, classifying cats versus dogs in image data.

**28:58** · And, in LLMs, of course we, we deal with texts.

**29:01** · So what is the class label here?

**29:03** · Or the thing we want to predict when we talk about "standard training loop".

**29:07** · So here that's really the next word in a text.

**29:10** · So like we talked about before.

**29:13** · The next word is what we want the LLM to predict.

**29:16** · So when we prepare the data, we have the input here and the target. This really the same as the input, but shifted by one position.

**29:25** · So when the model sees "in the heart of" the next word would be "the", for example.

**29:33** · So really just shifting everything by, by one.

**29:39** · And so usually we train for one to two epochs.

**29:43** · That's usually a good sweet spot.

**29:45** · Actually, most, LLMs are not even trained for a full epoch. Or sometimes you might read something like 1.1 epochs or something like that.

**29:56** · So just to take a step back, an epoch is one pass over the training set. But usually these training sets are super large and the models are distributed over multiple machines that it's not really super, I would say feasible to do.

**30:14** · The classic, I mean, you can, but not many people do that, do the classic epoch.

**30:20** · It's more like drawing random batches from the data set.

**30:24** · So there might be then overlaps and some batches are seen twice, some, not at all and so forth.

**30:31** · But if we think of the classic epoch regime where epoch means one pass of the training set, usually training for one epoch is what most people do.

**30:41** · You can train a bit longer.

**30:43** · I think there was a paper looking into that. Pythia, from Eleuther AI where they trained on duplicate, duplicated and duplicated data.

**30:53** · And they didn't see really a difference.

**30:55** · So here on some smaller scale experiments, I saw basically after two epochs, you see overfitting.

**31:01** · So overfitting means essentially, that you see a larger gap between validation and training loss.

**31:07** · So the model still improves on the training set, but, it doesn't generalize to the validation set.

**31:14** · So usually one to two epochs is the sweet spot.

**31:17** · You can train more and the model will actually still become better at generating texts that looks realistic, but it's also memorizing the training sets a lot at some point.

**31:29** · So it's basically just, yeah, repeating the training set, which is not a bad idea, because you can still, I mean, add some variety in the sampling.

**31:40** · So, I don't have slides on that, but you, when you implement the (text) generation, and basically you have settings like, top-k top-p and temperature scaling, where you can control the amount of randomness.

**31:52** · So it doesn't regenerate the training data. But, yeah, you can also just stop training earlier, especially if you have a large data set. And small, if you have a small data set, actually, I would say it almost makes sense to train longer until, you know, your LLM generates coherent text, and then you can control the memorization a bit more in the sampling.

**32:13** · So one, one challenge that LLMs also still have is what type of memorization is good, desired and which is not desired.

**32:22** · So I don't think there's a good solution yet.

**32:26** · What you almost want to do is kind of like mask, certain things to be memorized.

**32:32** · For example, if you think about ChatGPT, and a lot of people use ChatGPT for, you know, like, asking it history questions.

**32:40** · And of course you want the LLM to memorize historic dates. If it would make up, let's say the date for Independence Day and tell you it's, I don't know, December 12th, that would be pretty misleading.

**32:51** · So we do want the LLM actually to memorize certain things from the training set.

**32:56** · It's just that we also want ...

**32:59** · want it not to memorize everything because then it can generate, anything else that is not in the training set.

**33:05** · So that's like, it's a bit tricky.

**33:07** · I think it's an unsolved problem where we do want some memorization, but of course, we don't want to just, you know, copy paste training data.

**33:19** · So by the way, if you are interested in pretraining my colleague, Adrian, put together a Studi, on Lightning, on our platform, where it's basically, you don't have to worry about installing anything or the machines.

**33:32** · It's all in the cloud, but yeah, it's training a 1.1 billion model on 3 trillion tokens takes about four weeks on 64, a 100 GPU.

**33:43** · That's a lot of GPUs, but just as an example, and yeah, pretraining takes a long time. It's, uh, usually not necessary if you are interested in adapting LLMs for certain tasks.

**33:56** · Usually we start with a pretrained LLM. But yeah, if you're interested in pretraining, check out the Studio by my colleague, Adrian.

**34:06** · So, but that brings us also to the topic ... Most of the time when we work with LLMs, we work with pretrained weights.

**34:14** · So there's usually someone who was kind enough to share the weights openly.

**34:18** · There are many companies or research institutes who do that.

**34:23** · So, in LitGPT, the library I helped developing with my colleagues (Adrian, Carlos, and Luca), we support more than 20 LLM model weights, all based on the same model architecture, like I told you before GPT.

**34:39** · But of course with them slight architecture variations, but really, it's a lot of architecture variations, but yeah, we try to keep the code base readable so that it's actually also maybe a nice library to study the difference between certain LLMs.

**34:51** · So in any case, if you are interested in using that, you can actually download, weights by just \`litgpt download <the name of the model>\` And then you can chat, chat with it, finetune it, further pretrain it or pretrain it even from scratch or deploy it.

**35:09** · So, yeah.

**35:09** · Like I said, most of the time ...

**35:10** · Most of the time when we work with LLMs, we are not interested so much in pretraining, but, in adapting it for downstream tasks, for example, by finetuning LLMs.

### Classification finetuning

**35:22** · So here I have two steps for the finetuning.

**35:27** · There's one, the finetuning with class labels.

**35:30** · It's an example to develop a classifier, and then we will also talk about building a personal assistant.

**35:38** · So if you are interested, for example, in text classification, a popular example would be classifying if a text message or email is ham or spam.

**35:48** · So for that, I mean, it's almost like a classic machine learning problem.

**35:51** · You have a label ham or spam and the text you want to classify.

**35:56** · And all you have to do if you want to adapt an existing model so all you have to do is you have to replace the output layer.

**36:05** · So originally the output layer in this case of the smallest GPT model has 768 hidden notes, and then it maps to 50,000 output nodes.

**36:17** · So the output nodes here represent the size of the vocabulary.

**36:22** · So how many words are in this tokenizer that a model has been trained on.

**36:30** · And so what happens usually is that it maps from this back into the words.

**36:36** · But in this case, if we are only interested in classifying ham and spam, so we don't need 50,000 words here.

**36:43** · We only need 2.

**36:45** · So we can actually replace this output layer by a smaller layer.

**36:50** · So this one maps now from 768 to ham and spam instead of five 50,000, basically.

**36:58** · So it's just also for efficiency, really.

**37:00** · It helps really getting better performance out of it, helps with efficiency and so forth.

**37:05** · So it's very simple.

**37:06** · It's just like one line of code.

**37:07** · I have it in my GitHub repository, one line of code, you change this layer and then you finetune it.

**37:14** · And, so basically we evaluate it the same way as before.

**37:18** · We track the loss during the training.

**37:20** · This actually looks pretty good.

**37:21** · No overfitting, but in addition, now we have a target task.

**37:24** · So instead of just, you know, looking at the next word, what we can also do is we can take a look at the classification accuracy.

**37:31** · So classification accuracy here means, how many examples it classifies correctly.

**37:37** · So how many, if I have a hundred messages, and I classify 80 correctly, I would have an 80% accuracy, for example.

**37:47** · So it's, it's more like helps us to evaluate the, as a human, the performance of the model on the target task.

**37:55** · Now one might ask, why don't we just train the model to optimize or maximize the accuracy.

**38:03** · So that's unfortunately not possible because accuracy is not differentiable.

**38:07** · So we do still need the loss as the loss function to minimize during training Because yeah, we can calculate a loss derivative or gradient with respect to the model weights where accuracy is not differentiable.

**38:19** · So we can't use that (loss) to train the model, but we can take a look at that during training and then we can get an idea of how good our model is.

**38:26** · So here it's almost a hundred percent training accuracy.

**38:30** · Maybe I would say 97% validation accuracy.

**38:34** · And once you're done with that, you would also take a look at the test accuracy.

**38:39** · But by the way, also, we don't need to finetune all the layers.

**38:42** · I told you, you can replace that output layer and then finetune the whole model.

**38:47** · Actually you don't need to update all the layers during training.

**38:51** · So here I did some experiments and, for example, on the left-hand side, I'm only updating the last layer.

**38:57** · This is a slightly different dataset, so that's why the accuracies are/look a bit different than on the previous slide, but, so for reference here, you get about 75% (accuracy), if you only update the last layer, you'll get about, I would say 90 something percent, if you update or finetune all the layers. But you can see it's not necessary. Here YI'm only updating the last two layers plus the last two transformer blocks.

**39:24** · And you can say, okay, it doesn't really get better after this point.

**39:27** · So it really doesn't require updating all the layers.

**39:31** · It really it's enough to update the last few layers here and it's also actually faster.

**39:37** · So compared to finetuning all the layers where it takes the most time, updating only a few layers is twice as fast in this case, for example.

### Instruction finetuning

**39:48** · Okay.

**39:49** · So this was classification finetuning, but I think most people I would say are more excited or interested in probably instruction finetuning to create a personal assistants and chatbots and so forth.

**40:02** · And that's basically what ChatGPT is. Personally I would say, yeah, don't underestimate, classification finetuning.

**40:10** · I would say, personally, most tasks today, I would say, maybe not most ...

**40:16** · I mean, this is just me saying that, but I think many business tasks are really classification tasks.

**40:22** · If you think about, you know, sorting your documents, categorizing input emails, classifying customer sentiment, predicting whether a customer churns or not based on some text communication and so forth, I do think there are lots of practical business cases where it's actually a classification problem rather than let's say a chat bot problem. Of course, chat bots are also super useful for certain tasks, but they're more like general purpose where I think a lot of business cases they would be solved or can be addressed with classification finetuning, which is much cheaper and simpler to implement. But anyways, so let's talk about building a personal assistant using an instruction data set.

**41:09** · So for that, usually, when we are interested in building a personal assistant, like a ChatGPT likea chatbot. The data set looks like as follows, where we have an instruction and input and an output. And you know, this input is also optional.

**41:24** · You can actually also append that to the instruction.

**41:27** · It's really, yeah, it's, it's just like a matter of format, both ways work, but this is just an example of most common example.

**41:36** · So what we would do then is we would take this, data set and then we usually apply a prompt template.

**41:43** · And in this case, I'm using the classic, Alpaca-style prompt template.

**41:47** · So what it is doing is it's adding this text below is an instruction that describes a task of writing a response that appropriately completes the request.

**41:56** · And then it's basically from up here, the instruction nicely formatted.

**42:01** · And that is what we feed to the LLM.

**42:04** · So we have this input that goes into the LLM and the LLM then is supposed to generate the response here.

**42:13** · So here the response would be "great results were achieved by the team".

**42:16** · So the instruction is "rewrite the following sentence using passive voice", for example.

**42:22** · And so this is how an instruction data set looks like.

**42:25** · And usually, the data set sizes, I would say they range, I would say between, thousand to 50,000, to a hundred thousand examples.

**42:35** · So the Alpaca data set back then it was the first, I would say publicly available instruction data set.

**42:41** · It was about 51,000, if I remember correctly.

**42:45** · And, but also people showed, I think that data set was called Lima.

**42:49** · They only had 1000 examples and got, I think even better results.

**42:52** · It was more about, again, the quality versus quality quantity.

**42:57** · So it really depends.

**42:58** · I think the more, the better. you should, of course, but you know, you can get away with a thousand examples.

### Preference finetuning

**43:06** · There's an additional bonus (I would say) step, it's called preference tuning.

**43:11** · And this usually follows the instruction finetuning. Because this is already a long talk, I won't go into too much detail about preference tuning because it's a whole can of worms.

**43:22** · There are lots of, lots of techniques.

**43:25** · But in a nutshell, what preference tuning is all about is kind of to refine the responses by the LLM.

**43:33** · So when we have the input here, "What are the key features to look for when purchasing a new laptop?"

**43:39** · especially, when we control the random seed, for example, in an LLM, it can generate different responses. Or we can also provide a human-preferred response, for example. But long story short, there can be different ways you can answer this answer, right?

**43:54** · So there could be a more technical response, where it says when purchasing a new laptop, the focus is on key specifications.

**44:01** · It would describe the RAM size, the storage type and so forth.

**44:06** · And there is, let's say a more user-friendly response. It depends on the audience of course.

**44:10** · But so, it would then be more like, "think about how it fits into your daily life, choose a lightweight model that you, if you travel frequently" ...

**44:19** · By the way, personally, I have a MacBook Air because I do think it's actually a really good machine and I do have to travel a lot. So yeah, I, do like a lightweight laptop. For my work, for my job. I have a MacBook pro because it's, you know, I needed more for the development work.

**44:36** · So you know, it's different different considerations. An both, let's say are different responses a model might give, maybe a model could have also a response that includes both, but that could maybe be confusing for the user.

**44:51** · So you basically in preference tuning, you would choose one or the other and do that for a large number of examples to kind of like steer the model more into what's the behavior that you want it have.

**45:08** · So really just refinement of whether it should be more technical or more user-friendly. And actually in practice, it's mostly applied to safety.

**45:19** · So to improve the safety of a model.

**45:22** · So for example, not to give instructions on, let's say how to build a bomb or something like that, or not to use swear words and so forth, but then also, yeah, to improve the helpfulness as well to give complete answers and not abbreviate the answers and so forth.

**45:37** · So really it's, yeah, I would say a finetuning of the finetuning.

**45:40** · A finetuning of the instruction finetuning, essentially like a preference finetuning.

**45:45** · So, I have more, I've written articles about that, that cover some of the techniques behind it.

**45:51** · I don't want to go too much into detail here in this talk because it's a really long talk.

**45:54** · And I think this is a really interesting topic that deserves more time itself.

**46:00** · So, but here are, if you're interested, some resources, if you want to read more about that.

### Evaluating LLMs

**46:06** · So, one interesting and very important topic of course, is evaluating LLMs.

**46:11** · I showed you earlier, in the case of classification finetuning, how we can evaluate a classifier.

**46:18** · We can use the classification accuracy as a metric, but how do we do that actually with instruction finetuned and preference finetuned models?

**46:28** · So one thing you may have read about is MMLU.

**46:33** · So this is a number usually between zero and a hundred. And when, you know, when..

**46:39** · when OpenAI gives a webinar I mean a webinar introduction to the new model. Or Gemini, when the new version is revealed or people share that new model they usually give you an MMLU score.

**46:55** · So it's usually a score between zero and 100 and people use that to rank an LLM.

**47:00** · And this is, I would say for some reason nowadays, one of the most popular numbers to evaluate LLMs.

**47:09** · So what that number really means is also basically it goes back to a paper.

**47:13** · It's called "Measuring massive multitask language understanding".

**47:17** · And what it basically means is how good is your LLM at answering multiple choice questions.

**47:23** · So basically the input, a typical input in MMLU might look like, "Which character is known for saying to be or not to be, what is the question?"

**47:31** · And then for answers and the model should respond with one of those, for example, here in this case, Hamlet.

**47:39** · And, yeah, and then you basically, ... so you calculate the score based on the number of correct answers divided by the total number of answers to get kind of like an accuracy score from that.

**47:52** · So that's why it's between zero and 100.

**47:54** · And it's essentially saying, so a hundred percent score would mean that the model answers all the multiple choice questions in MMLU correctly.

**48:06** · So it's basically just multiple choice performance.

**48:09** · I wouldn't say it's terrible or something like that, but it's also not the whole story.

**48:14** · It's really just multiple choice questions.

**48:16** · And you might remember from college, how much we all loved multiple choice questions and how, you know, how good they are in determining how smart we are.

**48:27** · It's really just memorization in my opinion.

**48:30** · Anyways.

**48:32** · If you are interested in tasks or evaluating a model like that, I mean, I wouldn't say it's useless.

**48:37** · And, honestly, so I want to be clear, I really think it's useful as the metric because we can use that to really measure performance in terms of training.

**48:49** · I'm just saying it's not sufficient to only measure MMLU.

**48:53** · Usually you need a bit more than that.

**48:55** · So, yeah, but if you're interested, so we have also in LitGPT, for example, support for the Evaluation Harness (by Eleuther AI). With one line of code, really, you can evaluate MMLU and other benchmarks for a given model.

**49:11** · And so it would basically give you the score.

**49:13** · So for example Phi-2 only gets 24% on MMLU compared to let's say these here.

**49:22** · So you can say, okay, these models ... I mean, it makes sense ...

**49:26** · GPT-4 is much, much better than a 2 billion model like Phi-2.

**49:31** · But yeah, it's not the whole story.

**49:33** · So if we want to evaluate how good an LLM is, it needs to be doing more than just answering multiple choice questions, right?

**49:40** · So if we use ChatGPT, it can do grammar correction.

**49:44** · It can rewrite your text.

**49:46** · It can make up new stories and so forth.

**49:51** · So one other metric people use, or not metric, more like a platform or benchmark is AlpacaEval. And that is more like a way to measure the conversational performance of LLM.

**50:05** · So here, how that works is they compare, I think, yeah, see, I need an LLM to fix the sentence here.

**50:13** · Actually should be "Compare the response by GPT-4 Preview using" ... Oh no, sorry, it's actually correct.

**50:21** · So what I'm trying to say is this method works by comparing a given LLM to the performance of GPT-4 Preview, and then it uses GPT-4 based auto annotator to kind of, so it's basically saying asks GPT-4 "Hey, how does my model compare to GPT-4 Preview?"

**50:41** · And, it's basically doing that to calculate a win rate.

**50:46** · I think it's like based on how often is your given model better than GPT-4.

**50:53** · So in this case, if we look at GPT-4 Omni, it's 57% of the time better than GPT-4 Preview.

**51:04** · So in this case is a wind rate of 51.

**51:07** · So this is the length corrected version.

**51:09** · So you can, you know, you use either this or this version. But the bottom, but the bottom line is that GPT-4 Omni, according to this GPT-4 based auto annotator is actually better than GPT-4 Preview. The question is, what does it mean to be better, better in what is it more correct or does the answer look more, I don't know, attractive or something like that?

**51:33** · So that's also not super, I would say scientific.

**51:37** · But it is at least a useful thing.

**51:39** · You know, it's an another thing that you can add on top of, um, of the MMLU score and the other benchmarks.

**51:47** · What's interesting, I'm just seeing here is that GPT-4 itself only got 38%.

**51:51** · So maybe that means that GPT-4 Preview was better than GPT-4. So GPT-4 got worse over time or something like that.

**51:59** · So it's kind of funny.

**52:01** · Okay.

**52:01** · Moving on, there's another tool that people often refer to when talking about LLM performance.

**52:07** · And that is the LMSYS chatbot arena.

**52:11** · So here it's really more like a pair-wise comparison.

**52:14** · So, here it's basically a crowd-sourced evaluation where there are two models left and right, and there's also a known anonymous version where, you don't know what the models are.

**52:27** · So you use that thing and you get two answers and then you get two rates that you can say, "A" is better.

**52:32** · "B" is better.

**52:33** · It's a tie or both are bad.

**52:35** · And then based on that, it's computing.

**52:37** · a pairwise ranking here.

**52:39** · So according to that GPT-4o it's also the best model.

**52:42** · So basically if we take these things together, if I go back a bit, what was it here so we can see, okay, in this case, maybe Gemini Ultra is slightly better than GPT-4o, but I mean, there is a signal there because according to this one and this one, GPT-4o seems to be a pretty good model.

**53:02** · So, I mean, of course your mileage may vary based on what you're looking for in the model, but yeah, this is usually how LLM performance evaluations work like. I have also my own approach.

**53:16** · I think the other approaches are great, but in addition, something quick I can do on my computer is, but I mean, it's also not perfect because it's also, it can be arbitrary, but what I like to do is I use just the GPT-4 API to score my answers.

**53:32** · So basically I have a given input I have a correct output from the data set and then I have my model response.

**53:39** · And then I asked GPT-4 to score the response on a scale from zero to 100, and I get a score between zero and 100.

**53:48** · And usually, I mean, it's also pretty reliable in terms of saying which model is better if I would look at the results.

**53:54** · So it's just yet another way.

**53:55** · That's just my personal way in addition to the other ones.

### Pretraining & finetuning rules of thumb

**54:00** · So with that, I hope I gave you an interesting overview of what goes into building an LLM just yet to end this.

**54:07** · I wanted to also give you some rules of thumb.

**54:10** · So with that, I mean how do we, I mean, there are so many things I covered.

**54:16** · How do we make sense of them or what should you use for your given project, for example, I would say, so we covered pretraining from scratch. I would say pretraining from scratch, that's the most expensive thing and how I would say that's almost never necessary unless you're trying to develop a new architecture or something, or want to have full control over your LLM or something like that.

**54:39** · I would say that's not necessary.

**54:41** · I think this is really more like for research purposes or really, if you're a big company and want to establish your own foundation model, for example.

**54:49** · Continued pretraining is a process where you do actually do the same as pretraining, but you take an existing model and continue training that on a smaller dataset to instill new knowledge.

**55:01** · So this is, the pre-training starting with a foundation model is actually, in my opinion, one of the one of the most effective ways to instill new knowledge into an LLM.

**55:10** · So if you have a model that you know, can do certain things, do certain things, but it has no knowledge about things from 2024 because it has been trained in 2023.

**55:22** · So in that case, instead of training the whole model from scratch, you can just train it on additional data from 2024, for example.

**55:28** · So basically updating, finetuning.

**55:32** · We talked about special use cases, for example, spam classification that's useful for that, or I mean, in general text classification tasks. But then also to follow instructions, to build a chatbot and so forth. And then preference tuning is really to improve the helpfulness safety of models that are intended to be, for example, a chatbot.

**55:55** · So just to also give you an example where all these things are applied.

**55:59** · So there was this CodeLlama model by Meta AI, where they developed a model specifically for coding.

**56:06** · So basically here, they pretrained a model.

**56:09** · I mean, it's the same company.

**56:10** · So they, for this project, they started with Lama 2, but practically they also pretrained Lama 2, because it's done all been done in-house.

**56:19** · So the pretraining was the Llama-2 creation.

**56:23** · Then they had some more continued pretraining where this was more like trained on language and then they continued pretraining it on code specifically.

**56:33** · And then they had some more continued pretraining, for example, in this, so they develop multiple models in this one, they trained specifically more on Python code.

**56:42** · And then they had a stage where they trained on longer contexts and they call it finetuning, but it's essentially also a continued pretraining task.

**56:50** · And then the last step they had instruction finetuning to also create an instruction variant here.

**56:58** · And with that, I think we covered pretty much all of the stages of building an LLM from, coding the architecture, of course, without showing you too much code here or not any code, because it would be a very long talk.

**57:11** · otherwise. Talking about the pretraining and the finetuning.

**57:16** · So if you're interested, I have more, you know, concrete examples in my "Build a Large Language Model From Scratch" book where, yeah, it's applying all these stages in code.

**57:27** · So, yeah, to build your own small personal assistant.

**57:31** · If you're interested in that.

**57:33** · If you're looking for GPU solutions that we are at Lightning AI, we are building, um, the Lightning AI studio, which is the Studio environment.

**57:41** · You can use Visual Studio Code, Jupyter Notebook, and train models on multiple GPUs.

**57:46** · And what's nice also is you can flexibly switch between CPUs and GPUs for example.

**57:54** · So that's actually what I use for all my development work as well.

**57:59** · We also have a lot of examples on Lightning AI, so we have a lot of Studios to start.

**58:04** · So it's basically, you can think of it as almost like GitHub repositories, but they are already working.

**58:10** · You don't have to install anything like, package dependencies and stuff.

**58:14** · If you start a Studio, it's a, it's a template that already runs without having to install anything.

**58:20** · Yeah. And so we are at the end of this presentation.

**58:23** · So if you want to contact me, you can find me here.

**58:26** · And also if you would like access to the slides, they are here available on my website.

**58:31** · So I hope this was useful.

**58:33** · I hope it was not too long.

**58:35** · I have not checked my (wrist)watch, but I hope it is below let's say one hour.

**58:40** · And I hope this was an informative video.

**58:43** · Thanks for watching.