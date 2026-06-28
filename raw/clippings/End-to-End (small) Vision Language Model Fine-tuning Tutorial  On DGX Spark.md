---
title: "End-to-End (small) Vision Language Model Fine-tuning Tutorial | On DGX Spark"
source: "https://www.youtube.com/watch?v=_EMfJSmLSKE"
author:
  - "[[Daniel Bourke]]"
published: 2026-01-16
created: 2026-06-23
description: "In this video we fine-tune Hugging Face's SmolVLM2-500M Vision Language Model do structured data extraction from images.Because the SmolVLM2-500M model is is quite small in world of LLMs/VLMs, we're"
tags:
  - "clippings"
---
![](https://www.youtube.com/watch?v=_EMfJSmLSKE)

In this video we fine-tune Hugging Face's SmolVLM2-500M Vision Language Model do structured data extraction from images.  
  
Because the SmolVLM2-500M model is is quite small in world of LLMs/VLMs, we're able to do all of the training locally on a NVIDIA DGX Spark (see here for more: https://nvda.ws/4iQXZU4).  
  
The code should also run in Google Colab.  
  
If you have any issues, please let me know in a comment.  
  
Links:  
Google Colab Notebook - https://colab.research.google.com/drive/1yOwjCGZSq2jB4YLF0O0na2rEuqB6Nh7m?usp=sharing  
GitHub - https://github.com/mrdbourke/learn-huggingface/blob/main/notebooks/hugging\_face\_vlm\_fine\_tune\_tutorial.ipynb  
Learn Hugging Face Book Version - https://www.learnhuggingface.com/notebooks/hugging\_face\_vlm\_fine\_tune\_tutorial  
Dataset - https://huggingface.co/datasets/mrdbourke/FoodExtract-1k-Vision  
Base model (SmolVLM2-500M) - https://huggingface.co/HuggingFaceTB/SmolVLM2-500M-Video-Instruct  
Demo - https://huggingface.co/spaces/mrdbourke/FoodExtract-Vision-v1  
  
Livestreams (where I build this project from scratch):  
Part 1: Creating a VLM dataset - https://www.youtube.com/live/cZVU559BLLM?si=jyI9pWXxkmXMO9qq  
Part 2: Fine-tuning a VLM with LoRA and QLoRA and getting many errors (mostly my fault) - https://www.youtube.com/live/Lgcp9hBqWEM?si=gA\_7exPeqIwcxRYj  
Part 3: Switching from using LoRA and QLoRA (we’ll do these in a future video) to fine-tuning a smaller model (SmolVLM2) successfully, uploading it to the Hugging Face Hub and then creating an publishing a demo - https://youtube.com/live/cZVU559BLLM?feature=share  
  
Courses I teach:  
Learn AI/ML (beginner-friendly course) - https://dbourke.link/ZTMMLcourse  
Learn Hugging Face - https://dbourke.link/ZTMHuggingFace  
Learn TensorFlow - https://dbourke.link/ZTMTFcourse  
Learn PyTorch - https://dbourke.link/ZTMPyTorch  
  
Connect elsewhere:  
Download Nutrify (my startup) - https://apple.co/4ahM7Wc  
My website - https://www.mrdbourke.com  
X/Twitter - https://www.twitter.com/mrdbourke  
LinkedIn - www.linkedin.com/in/mrdbourke  
Get email updates on my work - https://dbourke.link/newsletter  
Read my novel Charlie Walks - https://www.charliewalks.com  
  
Timestamps:  
00:00:00 - Introduction  
00:02:19 - What is a VLM?  
00:03:45 - Why fine-tune your own model?  
00:06:05 - LLM fine-tuning mindset  
00:06:51 - Case study: Nutrify  
00:09:16 - Case study: Invoice Extractor  
00:11:06 - Ingredients and tools we're going to use  
00:12:16 - Exploring the FoodExtract-1k-Vision dataset  
00:15:52 - My setup  
00:16:13 - Dataset formatting for VLMs  
00:16:54 - Dataset Creation for VLMs  
00:17:20 - Getting a model to fine-tune  
00:18:13 - Our task overview (structured data extraction from images)  
00:20:11 - What we're going to end up with  
00:22:38 - Code Starts  
00:23:31 - Viewing a single data sample  
00:29:08 - Splitting our data into train and test sets  
00:34:25 - Inspecting our model's architecture  
00:40:03 - Reading the recipe of the SmolDocling paper  
00:45:29 - Freezing the vision encoder in our model  
00:47:34 - Discussing batch sizes  
00:49:06 - Setting up SFTConfig  
00:52:03 - Training our model with SFTTrainer  
00:54:11 - Model training starts  
00:54:19 - Model training finishes  
00:56:13 - Inspecting our model's loss curves  
00:57:10 - Uploading our trained model to Hugging Face  
00:58:19 - Model uploading to Hugging Face begins  
00:58:26 - Model uploading finishes  
00:59:38 - Comparing the base model to the fine-tuned model  
01:01:06 - Viewing our fine-tuned model's first predictions  
01:03:35 - Creating a demo with Gradio  
01:06:46 - Uploading our demo to the Hugging Face Hub  
01:07:35 - Trying out our demo  
01:08:27 - What's next and extensions

## Transcript

### Introduction

**0:00** · Ladies and gentlemen, welcome to the machine learning cooking show. In today's episode, we are going to fine-tune a small vision language model or VLM or MLLM multimodal language model. Multiple modalities, vision and language locally, specifically on the Nvidia DGX Spark. You can't see it from your angle, but I do have a a beautiful little gold box here. I'm going to do all the training on this machine here.

**0:26** · And so what we're going to do on the machine learning cooking show is uh step by step. If you want to skip to the code, jump down to the timestamps, but this is going to be a brief overview uh using the keynote and then we'll get through a walkthrough of the code. And by the way, this is a quick version. So I'm going to go relatively quickly through all the code here. If you want to go through a full walkthrough, I did code this live throughout this week. Uh I'll leave links to those and links to everything else that you need in the description. But let's discuss what we're going to do. We'll first talk about what a VLM is.

**0:55** · We'll download a model from HuggingFace, specifically small VLM2 500 mil. Now, I classify a small vision language model as a model that is under 1 billion parameters.

**1:09** · These are the type of models that are specifically designed to try and run on edge devices. Yes, you can run larger models on edge devices um such as GEMO 3N um at 5 billion parameters. However, I'm going to leave the small classification to those models that are under 1 billion parameters, and that may change in the future as hardware gets better and better. We're also going to download a data set because we can't fine-tune a model without a specific data set, right? That's going to be food extract 1K vision.

**1:36** · I also have a live stream of how I made that data set if you want a step by step, but we'll also see that shortly. We're then going to fine-tune the model using TRL transformers reinforcement learning in a supervised fine-tuning way. We'll upload our fine-tune model to hugging face so that we can share it and other people can use it. Uh we'll create a demo for people to interact with because we as programmers, we love to write code and interact with models with code. But a lot of people out there love to just drag an image into our demo and then try it out.

**2:07** · It's one of my favorite workflows is data or sorry data model demo. And then we're going to discuss extensions to make the model better. So what is a VLM? Without getting into too much depth, I'm going to leave two blog posts here and there are also some papers in there that you could read if you want to learn more about it. But this is the structure of a VLM and even the structure of the VLM we're going to work on today.

### What is a VLM?

**2:32** · You take some images and you take some text and you have a projector which combines the image and text input and then you have a text decoder. A decoder is what produces those tokens uh one by one. And so this is where a lot of uh modern LLMs are going. They they have a vision component, uh a language component, even an audio component, and some now are even doing video components as well. And so you're just putting all the data into one big model. But um a lot of the time there'll be a specific image encoder.

**3:03** · So in our case we're going to use SIGLIP 2.

**3:08** · Well at least that's what small VLM uh 2 uses as the image encoder that reads the images. Then the text gets turned into text embeddings. Then we have a projection layer which merges those two into the same embedding space and that goes to the text decoder which is an LLM in our case small LM2 and then we get our answer. But we'll see this in practice later on.

**3:31** · Now, why fine-tune your own model?

**3:33** · Number one, of course, is ownership. Own the model. It can run on your own hardware. The data stays local and private. Again, everything that I'm running in this video is going to be uh within this room here. It's running on the Nvidia DJX Spark that's on my desk.

### Why fine-tune your own model?

**3:48** · It's simple. If your task is simple enough, you have a repetitive task that you want to do over and over again, you can just use a small language model. You don't need the biggest model via the API. of course get started via uh an API, but if you find that you're doing a repetitive task, you might find that you want to train your own model. Or if you're a business and you need to keep your data private, well then you definitely probably want to look into training your own model for uh a repetitive use case. Infinite inference.

**4:16** · So because we don't need any API calls, this model can be run offline. We could turn the internet off and run it on a phone for example um in the field. I just had a project with a a client where I needed to train a model that had to run uh computer vision. Uh I used an object detection model, not a VLM, but it needed to run in a setting with no internet connection. Uh so that's where infinite inference comes in. You don't need API calls. Batch mode for scale. So you can run this model in batch mode to get faster inference um than single API calls. Yes, you can do batch with APIs.

**4:50** · However, this of course still requires API usage, which in turn usually costs dollars. Um, what would you use batch mode for scale?

**5:00** · Say we have a specific VLM that's designed to extract uh extract structured data, which is what we're going to focus on doing today. We could run that over a large image data set to extract uh target images that we're looking for. So, filtering a large data set is one of the best use cases for this. Number five, make base models much better. So, why fine-tune your own model? Oftent times when a base model gets published, and I'm using the term base model or pre-trained model, they can be used inter interchangeably.

**5:27** · Um, when a model gets published, it usually works fairly well on different benchmarks, but I want to introduce you to the beautiful power of fine-tuning is oftent times, uh, if a model performs okay on benchmarks, that's a good sign that if you feed it your own custom data, it will definitely improve on your own custom data. So, that's something to keep in mind. And, uh, here's a a note.

**5:54** · This is a mindset I'd like you to get into for LLMs and VLMs. They are tokens in where a token is a numerical representation of data. Whether that data be text, images, video, audio, you name it. It gets represented as a token.

### LLM fine-tuning mindset

**6:07** · How you tokenize it will of course depend on the model you're using.

**6:10** · Luckily with hugging face, all the tokenizers load in, but you just need to think data turns into tokens. Tokens and numbers. Computers like to understand numbers and recognize patterns in numbers. And then tokens out. So we have our tokens in. In our case is going to be uh images of food and not food. And we'll see this later on. And then tokens out, which in our case is going to be structured data. So if you have this idea of tokens in, tokens out for LLMs and VLMs, you can create your own specialist model by thinking of your own data sets in a format of tokens in tokens out. What tokens do you have now?

**6:44** · What tokens would you like out?

**6:47** · So specific use case, Neutrify. This is an app that my brother and I uh build.

### Case study: Nutrify

**6:52** · It's live on the app store. It's not a fake app. It's a product in production.

**6:56** · neutrify.app. So I take a photo of my lunch that I had the other day. Neutrify is designed to recognize whole foods. We don't do barcodes. We just do images. So that got sent off to Gemini. And as you can see there, right? So it took a few seconds to load because that's going from an image to Gemini, which is an API, and then taking a photo. There we go. So it produces JSON, and then we get food title. Um, sardines with pecans, dates and pickles, which is absolutely correct. Sardines, pecans, pickles, dates.

**7:27** · Um, I just want to show you this is a vision language model, right? So on the back end of Neutrify, we have image to Gemini and text to Gemini and then Gemini outputs this. One of my goals for the year is to be able to replicate this workflow with an ondevice model. So we actually don't need an API call. This can run locally on device. And so the model we're going to train in this uh small video, small tutorial is the first baby version of that. So that's a specific use case. If you want to check out Neutrify for tracking your whole food intake, go to um neutrify.app.

**8:01** · Here's another example use case of we take a photo of an ingredients box or ingredients package. And this is Gemma 3N which is a 5 billion parameter model.

**8:12** · This is using Google's AI edge gallery.

**8:15** · This is running directly on device. I forgot to turn my Wi-Fi off, but this is uh an example of a VLM running on device. But as you see, the outputs aren't really that perfect. Now, of course, we could probably upgrade this with uh prompting, but we could also fine-tune. I'll save this for a future video, Gemma 3N, because it's quite a large um VLM in terms of hardware requirements. We might save that for a video where we focus on Laura/Qura, but that's for another topic. If you'd like to see that, leave a comment below.

**8:47** · And so we could fine-tune it to specifically extract the ingredients that we want rather than all of this extra information such as the address.

**8:56** · Now, the beautiful thing about this is that it was quite quick, right? And we also got to see it happening live. So, as a user, that's a great experience.

**9:05** · And again, as I said, this is running on device. So, I could turn my Wi-Fi off or be in a supermarket with low internet connection and that would still work.

**9:14** · So, here's another specific use case. If I was running a business called machine learning and muscle, right? We're making all kinds of gains with both our muscles and models. Um, that was cringe, but anyway, here's the project details we had. There's my consulting services rate, total. And then what if we were a business and we get like a thousand of these invoices a day or emails? We could extract to JSON. So, this is what I mean by structured data. This is an image.

### Case study: Invoice Extractor

**9:43** · This is the structure we want. So what would this look like? Of course, it would fill this out. And now we could put this into a database that we could easily access uh such as an Excel spreadsheet or a pandas dataf frame or something like that. And in fact, let's try this out. Hey, so if we go to um Gemini, let's upload our invoice test images.

**10:07** · I just want to show you if we get the invoice that this is a um please extract the invoice details to JSON. Now I'm not I'm going to use a fast model which is Gemini 3 flash.

**10:29** · I'm not um giving it a structure because I just want this to be quick. Uh we could put this as quick.

**10:38** · There we go. Look at that.

**10:41** · That's basically exactly what we wanted.

**10:44** · Right now, this is using Gemini, but if we had confidential information that couldn't go to a Gemini model, this is where we could create our own custom VLMs for doing structured data extraction from images. So, there's the image, there's the structured data. So, if we go back to the Keynote, let's keep going. So, here's the ingredients we're going to be cooking with. We have a base model which is small VLM2 500 mil uh video instruct.

### Ingredients and tools we're going to use

**11:12** · This is one of the smallest VLMs that you'll find uh available on hugging face. There is an even smaller version and in fact that could be an extension for you is to see if this workflow could be used with that. We have a paper that we're going to be drawing information from and this is a beautiful uh beautiful thing about modern machine learning and AI is that all of the latest and greatest stuff often gets published to research and then I mean look at this. This was published March nearly a year ago, right? But it took a while to trickle down into uh like coding libraries and whatnot.

**11:41** · And a lot of the innovations around small dockling is what we're going to sort of see and practice firsthand and the code coming up. And that's uh putting together a data set in a format that you'd like.

**11:56** · That's where a lot of the effort goes into. And speaking of data sets, we have uh a data set which I've created from scratch which is food extract 1K vision and we'll have a look at that shortly.

**12:07** · So oh actually let's look at it now while we're on the topic of data sets.

**12:12** · So this is our data set. We have only 1500 samples which is quite small in comparison. The small dockling paper here we go which fine-tuned uh 256 mil.

### Exploring the FoodExtract-1k-Vision dataset

**12:26** · There we go. small dockling uh fine-tune small VLM 256 has millions of samples.

**12:34** · So if we go down, they have a data set spread. Yeah, there we go. So this is how many samples they used in their data set. So I would say that's about 20 million or so without actually totaling them up. We could pass this to Gemini as a multimodal model and say total up the number of samples.

**12:58** · Okay, so they're using way more than us, but we're going to start small with only 1,500 samples. And more specifically, ours are 1,000 images of food from food 101 and 500 images of not food because we want to train our model. These are called hard negatives in the business, right? We want to train our model to be able to uh not only detect food and food types, but also hey, if someone uploads a a photo of their computer, we don't want it to be outputting um information about what food is there.

**13:28** · And so the labels I were generated um sorry I generated the them synthetically by prompting quen 3VL8B instruct. So we are essentially distilling a larger model uh an 8b parameter model 8 billion parameter model into a 500 million parameter model and what's that reduction of about uh 16x. So quite a quite a large reduction and the goal here is to get structured data out like this.

**13:58** · So if you remember the Neutrify uh video that we showed before, this is what we could do. Image title, food items, and then we map these to a database or we just run this model at scale over a large image database to extract the food images. So let's look at a single sample. So if we go to here, we got a delicious is that a frozen yogurt? So it's ice cream and a macaron.

**14:22** · And this is the JSON output that we're going to get our model to predict. So given this image, we want to fine-tune our model to predict this. And remember what what did I say before? LLMs and VLMs are tokens in tokens out. So our image is going to get tokenized, turned into a token uh format. And this uh is going to get this is what uh sorry our model is going to predict this output label JSON as tokens. And ideally it's going to be in this exact format.

**14:52** · So we can easily just load this into some sort of database. Um and so there's some metadata here about this. I'll let you explore this data set. It's uh available on um hugging face data sets. I've also got a live stream of how I created this.

**15:08** · But if you want to see more data set creation in the future, please let me know. So we've got a base model, a paper that we're going to follow some instructions from, and a data set tools.

**15:19** · We have the TRL library. That's what we're going to be mostly using, which is of course backed by hugging face transformers. I'm going to be running all of this live on an Nvidia DGX Spark.

**15:30** · Um, but you could also run this on Google Collab because we're using quite a small model. You can use uh Google Collab. And in fact, the notebook we're going to be working on, the link will be below, has a big button here that if you want to open it in Collab, you can do that there and run this along. So, but as I said, I'm going to be using the Nvidia DJX Spark. This is my setup right here. That's what I'm coding. This is where all our computes going to run. And this is my Mac Mini. I'm uh running code on the Mac Mini or writing code, sorry.

### My setup

**16:02** · And then running it via SSH on the DGX Spark because we get the CUDA ecosystem on on this and it's just yeah, it's a beautiful little machine.

**16:12** · So, let's discuss data set format.

### Dataset formatting for VLMs

**16:15** · really important thing uh when working with any model is having a data set. But the without going into too much depth for a VLM vision language model you need vision components and text components language components. So in essence our data set is just going to be an image and text as in we'll feed it a prompt saying extract uh XY Z from this image.

**16:37** · So that's it image and text pairs. Nice and simple, right? If you want to read more about that or how to use um create your own data sets, I've got a link here um uh in the notebook for the TRL vision data sets format. But this is essentially what you'll see, right? Uh if you want to see how I created the data set, I used the hugging face data sets image data set format. And then we've got a a live stream here uh where I went through and basically built this data set from scratch. You can see it over here.

### Dataset Creation for VLMs

**17:06** · And there I've just highlighted a little point where we've uploaded it to the hugging face hub. And that's exactly what we just saw before.

**17:15** · So where can you get a model? You can get a model at one of my favorite basically my homepage huggingface.co/models.

### Getting a model to fine-tune

**17:24** · So if we go to the front page and if we go to models and then another way of saying VLM is image texttoext. So these are all the recent ones. You'll notice the uh number here is number of billion parameters or sometimes it'll have million. Again, all of these are quite except for this one. It's about a billion. My definition of small is under 1 billion. So, for example, Google just released medge gemma 1.54b.

**17:53** · And that what's the size of this? Uh that's close to let's say 9 GB, right?

**17:58** · To run. You could get it smaller with quantization, but this is designed to extract medical information from medical images. We want to go even smaller, but that's just where you find models.

**18:11** · And then this is our task. We have structured data extraction from natural images. This is called food extract vision. We have a food 101 image. The ideal output here will be JSON. We want our model to output exactly this. But I want you to just think in your head this this input here much like our LLM video

### Our task overview (structured data extraction from images)

**18:32** · can be any image and this output here can be any structure right you don't might want to not with a small model you might want to not output I guess something that's 20 times as long as this because it might not work as well but small dockling actually works pretty well and that can output up to three pages of text so hey give it a shot why not but the principle here is we are just having image and text pairs. And you might be thinking, Daniel, can you just train a classifier onto this to classify uh food and not food images?

**19:05** · And you'll be exactly right. We have actually done that in Neutrify. That's what runs live over the camera. It runs at about 300 FPS. It's a fast model. But the beauty of VLMs or LLMs in general is they have the unbounded output. because they have the decoder output, you can output any tokens you want as long as you've trained the model to output that format of tokens. So, we can get not only classification, but a title and food items and drink items in one shot.

**19:35** · And so, thank you for Tron Lee for this beautiful photo of Switzerland uh on Unsplash.

**19:40** · And where could we use this model? We could use this model to filter a large data set of images for food items and drink items such as data comp 1B. That's 1 billion images uh on hugging face or on device as a food drink extraction model. So remember the goal of with Neutrify app uh to replace the Gemini dependency with ondevice models. So our final outputs of what we're going to finish up with this tutorial.

**20:03** · If you go through the end to end, you will have a food extract vision small VLM2 model fine-tuned and you will have a demo publicly sharable demo that you can both access right now if you'd like to as well. So without any further ado, let me just show you the demo or the sorry the fine-tuned model. There we go. That's on my hugging face profile. And here is the demo. No spoilers. Um but I'll show you how it works.

### What we're going to end up with

**20:32** · So, if everything goes to plan, the original model now, it takes a few seconds to load because we are running on a free GPU here. Actually, I might have to refresh this. Sorry. I think I rebuilt it. Okay, there we go. We try the demo. There we go. Okay, so the original model not fine-tuned. We have this input prompt to tell it to extract classify the given image into food or not food. Right? We give it this input prompt and the model just outputs this.

**21:04** · But our fine-tune model knows that it's not food, so it gives it a zero. And then we have the fries. All right. This is what I cooked for dinner the other night with some beef tallow on there.

**21:19** · Beautiful. So the original model outputs that. So an empty list, not what we want. And then we have the fine-tune model which has is food image title French fries. So very quite a simple use case but very useful for uh my particular task which is um getting structured information from food images.

**21:40** · So as I said if you want the notebook um or I haven't said this part yet you can go to learnhuggingface.com all the code and write up will be available there. So we've got that in a book form. You can go through it scroll through it nice and just read all the information that we have there. I've linked a bunch more resources as well as um some shoutouts. So, there's some great resources. Where do we have it here? Oh, yeah. So, there's some great docs on the Hugging Face website. Um there's also uh Google Docs example of fine-tuning a vision model for GEMA 3N.

**22:15** · There's a a blog post on Laura, but that's for a future video. If you want to see that um please let me know.

**22:22** · Now, let's get started. the code on GitHub if you want to run that there.

**22:26** · They got links to all the live streams.

**22:29** · But I'm going to now jump in locally to VS Code.

**22:37** · And this is just the notebook. I'm going to restart that. I've just got this running on my hardware. Let me just show you this Nvidia SMI. This is uh Nvidia GB10.

### Code Starts

**22:49** · Grace Blackwell 10 uh which is what the DGX Spark is running here. So let's get started.

**22:59** · We'll run some code. We have some import dependencies. Uh we actually don't need bits and for this because we're not using Laura, but in a future one when we train a larger VLM or a larger LLM, we'll definitely be using Laura. So which is low rank adaptation. So let's run this.

**23:18** · We have CUDA. We're going to load our data set.

**23:24** · And we're following the motto here of data model demo. Data model demo. So if we have a look at one of our example samples from the data set, we get some fields here. I'm going to zoom quite far in so that way you can see what's going on. Uh image ID. This is all metadata here. The main things we care about here is the image and the output label JSON.

### Viewing a single data sample

**23:45** · So we want to give our model this image.

**23:46** · our uh base model and we want to fine-tune it to produce this output and this output has been produced by Quen 3 VL8B as a synthetic data labeler. I trained that or not trained that sorry I produced these labels on the RTX 4090 um for another project previously and I've repurposed them for um this VLM fine-tuning.

**24:10** · And so we get some image and text pairs.

**24:13** · Let's have a look at an example. might zoom out by one. So this is our example desired output is food one. So one or zero for food or not food. Image title a simple food t uh image title that is.

**24:26** · And then we have food items and there's no visible drink items. Again these are all produced by Quen 3 uh VL8B. If we wanted to turn this into a production system we'd probably definitely create our own handlabeled data set of about a thousand images and then we can test it on those handlabeled images. So we have some toast, some dipping sauce, herb garnish and cheese wedges. Okay. Now format data for use with a VLM. As I said, there is uh some docs.

**24:59** · Let's go TRL vision data set.

**25:04** · This is the format that we need.

**25:10** · vision data set.

**25:14** · There we go. So, we need it in something like this content as a message. And so, they give an example data set here, but I'm just going to show you what ours looks like. We're going to give it a symptom uh system message. So, you are an expert food and drink image extractor. Uh in a future video, I would like to train it without these two prompts. So, we just go from image to output. But for now, we're using some input prompts as well. So, you are an expert food and drink image extractor.

**25:43** · You provide structured data to visual inputs classifying them as edible food or drink or not, as well as titling the image with a simple food, drink related caption. Finally, you extract any and all visible food or drink items to list.

**25:54** · And then we have a user prompt. So, the system prompt is basically getting the model ready. The user prompt is what we would type into say a Gemini or Chat GPT in interface.

**26:05** · So classify the given input image into food or not. And if edible food or drinks items are present, extract those to a list. If no food or drink items are visible, return empty lists. So I don't if it's there's no food, I just want empty lists. Only return valid JSON in the following form. And then we've got our JSON structure. And then we give it some information about what we would like there. So this is just the code version of that. And then here's where we format our data. So this is just going to take a sample in from our data set.

**26:34** · If we look up here, right, one of these rows, okay, because this contains uh all the information that we need here, this is just going to take in one of those samples and turn it into a dictionary with the messages key. And then inside the messages, we're going to have our first message there, which is the role of system message, which is going to be that prompt up there. Uh and then we're going to have the role of user which is going to be this is our image and text pair. We have an image and then we have our text. So there's our text, right?

**27:06** · And the image of course is if we go to our example sample is in uh the image field. So if we view there, so right now it's in pill format. So Python image library. And then if we scroll back down, we have one final message and that is the model. So this is what our ideal model output would be.

**27:29** · Notice that it's an assistant. We've got user and system. We want to train our model to predict this output here. So the sample output label JSON. So given this input, we want our model to predict this output. Now what would that be in terms of machine learning speak?

**27:47** · If you don't know, that's okay.

**27:50** · That is a supervised fine-tuning problem. What I mean by that is that this is the ideal output and this is the input. In a supervised fine-tuning, so SFT problem, we give our model uh examples of inputs and outputs and then it figures out the patterns to bridge them together. So this is our example ideal output. This is our example ideal input. And our model is going to figure out the patterns to bridge those together. We don't tell it how to do it.

**28:16** · We just go, hey, here's my inputs.

**28:18** · Here's my ideal outputs. You predict what's between those two. So if we format our sample into messages format, we get uh a little bit of a convoluted structure here, but the good news is hugging face transformers uh and TRL handles this pretty well behind the scenes. And there may be slightly different formats for different models, but this is pretty universal for VLMs with transformers is the image and text pairs. Now a little note, I tried map.

**28:47** · So usually you can do data set.mmap um the format data function that we have up here this helper function but for some reason that would get stuck. Now if anyone knows why that might be or you have a fix please let me know. I'd love to hear uh we're going to create a training and validation split. So this is the 8020 rule in essentially we're going to use 80% split for training. So our model's going to use those to train uh and then 20% for validation or testing. Our model won't see those during training.

### Splitting our data into train and test sets

**29:15** · That way when we evaluate our model on the validation data set, we can get a good idea of how it's performing on unseen data because that's our ideal use case. Right there we go. Oh, excuse me. Where'd we go? Oh, data set pre-processed. I forgot to run this one, didn't I?

**29:35** · Getting too excited here.

**29:38** · Okay, training validation split.

**29:40** · Beautiful. So, here's an example from each. Now, these are pretty convoluted because uh for me that's personally a little bit hard to read. I could do it if I step through it. I also know what the data set is. Um but if you want to read through those, there's a bit of a a better formatted version on the book version of the course. So, if we go load data set, if we look there, you can start to see the output format there. So, let's jump back into the code. Up next, we're going to one of the first things I like to do is run a sample through a base model.

**30:12** · So get as quickly as you can, as quickly as you have a data set. Try out your base model. In our case, our base model is small VLM2 500 mil. Now, what do we want to pass our model? We want to pass our model only the image and text pair. We don't want it to see the output. So the assistant roll up here, where is that?

**30:35** · Assistant, we don't want it to see that.

**30:37** · We only want to pass it in the image and the text because that's what it would see in production, right? Just the image, just the text. This is our ideal output. So, we're going to keep that hidden from our model uh unless we're training it. So, this is where I just extract the first two messages. So, we have system and user. Notice that the assistant message is missing now. Now, we're going to load our base model. So, if you watch all the streams, you don't have to. I'll just tell you now. Uh I tried Gemma 3N. It's actually quite a good model for 5 billion parameters.

**31:09** · Probably a little bit um too good for our particular task. The reason why we're fine-tuning is we want a small model that isn't that great to make it great by fine-tuning it. So, we definitely could improve GM3 with a little bit of fine-tuning. Um but for now, it's uh I'll save that for a future video where we use a technique called Laura, which works better on larger models.

**31:29** · Um so if we load it in a pipeline now pipeline from transformers is a great way to just instantly uh start inferencing uh but as we'll see in a second we will want to load it as a model using the automodel class or one of the automodel class when we want to train it. So pipeline excellent for inferencing but for training and fine-tuning you want to use an automodel class. So we're loading this pipeline here. Now I have the model downloaded so it's already cached.

**31:59** · If you don't have it downloaded it will download this model. Um so it may take a minute or so depending on your internet connection.

**32:07** · And we can just pass in the base model uh or sorry our example. So let's remind ourselves of what this looks like. We're just going to pass this into the model uh into the pipeline. We're going to tell it generate 256 tokens max um new tokens, right? And then we're going to see the output. And the beautiful thing about the pipeline is that it handles all the formatting and pre-processing behind the scenes. So let's do that base model.

**32:35** · So that's the input there. And then the output, it's not that great, right? So our desired output is uh is food image title cheese plate. We saw that before.

**32:46** · So we can safely say that our base model is not that great. Can we make it better with fine-tuning? Well, we're going to have to see. So check our image. Yeah, that doesn't match this. This does match that. So that's our mission.

**33:05** · Now we're going to load the model without using pipeline. So I showed you pipeline because that's an easy way to start doing inference. That's probably the one of the quickest ways you can start exploring with different models, whether it be on a DJX Spark or Google Collab. Now let's load it with the autoprocessor and auto model uh for image text to text. Remember on Hugging Face they call uh VLM image text to text. So image and text to text. So let's load it. There we get our model and processor.

**33:35** · The processor is what's going to turn our images and text into the format that our model needs.

**33:46** · So this is because I've already downloaded this. It's just going to start loading that into memory. And let me just show you um files and versions. This is what it downloads. So we got the model.safetenses 2 gigabytes there. Uh we have the pre-processor config processor config. All the different stuff in there is basically settings for our model. Now if you'd like to learn more about those, I'd encourage you to just go and click through these. Right?

**34:11** · This is all available publicly. Um there's going to be a fair bit of information overwhelm, but with practice, you'll start to understand um what's what all of these little components do. And as I said, this is the quick version, so we're not going to discuss every single small thing. But if we expect uh inspect our models architecture, you'll notice a few major things.

### Inspecting our model's architecture

**34:31** · So we got the overall model, then we have the vision model, then we have the connector, then we have the text model, then we have the LM head, and then in between all of those we have smaller layers. So if you ever heard of a neural network, it's made of multiple layers.

**34:48** · Um, this is made of multiple models and which is in turn made of multiple layers within those models. So if we go back to our keynote, let me just give a quick overview of where we're at.

**35:01** · If we remember this diagram right from the start which is from one of these blog posts. Uh we have the image encoder that is in our case the vision model. We have the multimodal projector which is the connector. Remember how we have to connect the text and image uh numerical representations. And then we have the text decoder which is the LM head. So if we jump into back to our code there we go. Vision model connector text model LM head. Wonderful. If you want to read more about those, you can go there.

**35:33** · Um, in our case, the vision model uses SIGL lip, right, which is a great uh vision encoder, but it's also been trained on language. In the text model, in our case is small LM2 360 mil instruct the connector. So, this is what merges u of oftent times it's an MLP, the vision and text model. And then we have the LM head, which is going to output those tokens that we want. Now if we wanted to run inference uh using just the model and processor we have a few more steps than just running it via pipeline those are represented here.

**36:05** · So first and foremost we have to apply the chat template. So um that's going to apply some special tokens. Um if you want to see what that looks like we can just go here info chat template. I like to print out as much as we can when we're getting familiar with different things.

**36:26** · And then we'll print a new line. Or maybe we'll go down there.

**36:32** · And then we're going to pass it uh with torch nrad. So that means we don't want to use gradients. We're going to call model.generate. We're going to pass it in all of the keys from the example chat template. Again, max new tokens is going to be 256. And then we're going to filter it for um the generation output.

**36:50** · We only want the output that the model has generated. So we index uh for everything um from our input and beyond.

**36:57** · So say our input is 400 tokens. We want everything beyond that because we don't want to see uh our model is going to take our input and then generate new tokens. So that's what we want as the output. And then we're going to decode because remember um models and machines like numerical representations. And so when I say a token it's literally going to turn the text into a series of numbers. could be 125, 1, 6, 30,000, etc. We'll see an example of that later on.

**37:27** · But then we're going to turn it back into text and that is what decode does.

**37:31** · But let's not spend all this time talking about it and let's see about it.

**37:37** · So we got a few things here. Now this is our full chat template, right? Chat template. What are the pixel values? So remember when we have a vision model that is what's going to encode our image. So that has been encoded into pixel values into a tensor a numerical representation. So if we keep going down there's a lot there. Then we have the attention mask right which is all ones because we want if we multiply each of those pixel values by one it means we want to attend to those. If they were zero it means we were blocking them out.

**38:10** · Then we have input ids. This is where our text has been turned into tokens.

**38:15** · And remember how I said they're going to be a long series of numbers. There's probably a fair few there, right? I'm not going to read them all out, but I'll let you inspect those if you want. And again, they have an attention mask of all ones because we want to attend to all of those. That's the attention mechanism. If it was zero, it would say ignore these. Now, this is the raw numerical token input to our model. Uh this is just me filtering on input IDs.

**38:39** · So there's our series of tokens. These dot dot dots means that there's many more. Same with these dot dot dots. This is our pixel values. So this gets encoded by our vision model or created by our vision model. Um and then if we keep going down, this is what's going to go into our model. This is the human formatted version. So notice how we have uh IM start which is um instant message start or maybe I don't know exactly what IM stands for but this is the start, right? We have our image tokens.

**39:06** · Now, something to note in VLMs is that these are just placeholders. So, this is just going to tell our model, hey, pay attention to the pixel values rather than the image um placeholder tokens.

**39:20** · But that's getting a bit deep into that.

**39:22** · Just think of these as placeholders. Our model's going to look at the pixel values, not these image tokens.

**39:28** · Um, and then we go here. This is our text. Again, this is human readable.

**39:33** · This is not what our model is going to see. Our model is going to see a big chunk of numbers. And then this is the outputs from the base model. Uh nothing right because it's not fine-tuned to what we want. So there's a little note here on the image special tokens. So prepare the model for training. Now without going into the full paper, I just want to show you where I've got this little technique from. And we started this by saying welcome to the machine learning cooking show. And that's what I really think machine learning a lot of it is is uh it's like cooking.

### Reading the recipe of the SmolDocling paper

**40:07** · You have ingredients, you have a method, and then you have an output.

**40:11** · Right? So in this case, their data set was their ingredients. And small dockling is a model to extract structured data from text. And they actually use the same architecture that we're using, a structured data from um documents. So this is what small dockling produces, right? Structured data from uh OCR, optical character recognition. It's going to predict this uh sorry predict this given these inputs. So that's its recipe, right? And the data here is the ingredients. Excuse me.

**40:45** · These are the ingredients to small dockling. Whereas in our case, our ingredients are food images and text outputs. And so what did Gemini come to the count of? Total 27 million samples. Okay. So whether that's right or wrong doesn't really matter. It's probably in the ballpark, but a lot more samples than what we're using. We're only using 1,500. But the important thing is if we come down to this, they used 64 Nvidia A180 GB GPUs uh for four epochs requiring 38 hours.

**41:19** · So 4\* 38 what's that about 160 there. So 152 um with Atom W optimizer. These are all little tidbits and settings like in the formal way it's probably called hyperparameters. Well, it is called hyperparameters. Come on Daniel, use the correct terminology when we want it. But uh as cooks, we would read this and go, "Hm, that's something cool to try." And so that's a lot of what machine learning is, is finding a recipe similar to yours and then tweaking it to your own sort of liking, which is what we've done with food images.

**41:50** · They've used a learning rate of 2 \* 10 -4. We'll see that later on. Um for the vision encoder once unfrozen, now that's a that's probably the most key point there, right? It's hidden in four words. The vision encoder is frozen. We also employed gradient clipping to 1.0. We'll see that later on in the settings. And a warm-up ratio of 0.03. If you want to read through this paper, I'd highly recommend it because it's what we're basing a lot of our practice off. And the small dockling model works really well.

**42:20** · So um so as per the small dockling paper section 5.1, we're going to freeze the vision model.

**42:28** · So freezing means we're not going to update it during training. So we're going to freeze its gradients. So when our model um sees examples right inputs and outputs uh there's an optimizer which is called Atomw is going to go hey that output you produced from that input wasn't that good and then it's going to tweak the model parameters we have 500 million to play with uh the vision ones

**42:50** · are going to be frozen because that's the recipe that the small dockling team found to work and in fact I tried to train this model without the vision model um frozen and it didn't produce that great a results and spoiler alert I followed the paper um which said hey try this freeze the vision model and then it did work pretty well. So one of the things that you don't see with this notebook is all the experiments that I've tried behind the scenes. So there's run one, run two, run three, that's another model.

**43:20** · Uh run five, run six, run one, etc., etc., etc. And I can't imagine how many of the same were done for a research paper like this. So just keep that in mind with machine learning and AI in general. It's very experimental. For everything you see that works, there's probably a hundred or a thousand experiments that didn't make it to the published version. So just keep that in your mind. Keep experimenting. Keep trying new things.

**43:48** · Um we're going to freeze the vision model. So it's its weights, its patterns aren't going to update during training.

**43:54** · Only the rest of the model is. So the language parts of the model, if we had a larger data set, ours is quite small at a thousand training samples, we could have potentially performed two-stage training, which is what they did in the paper. Number one, they trained with a frozen vision encoder to align the LLM proportions to the model uh to the LLM portions of the model to the output um to the output. This is typo here, excuse me, to the output. Now, this is our desired format.

**44:21** · We want to align the LLM with our desired format because our format is unique, right? That's why we're fine-tuning it. Number two, we want to train the whole model to uh this is stage one. We do that and then once we've aligned the LLM, we train the whole model including the visual model to align all our features to our target data set. Now, for now, we're going to keep it simple and focus on stage one.

**44:45** · If you want an extension, you can go to stage two. I've left some code here um in the notebook that you could try out yourself. So how do we freeze a part of our model? Well, first let's count the overall parameters and trainable parameters in our model before and after freezing the visual vision encoder. So remember what our model looks like.

**45:04** · Model looks like this. If we want the vision encoder, how can we access that?

**45:08** · Well, this is a Python object, right? So we can go model dot vision model.

**45:16** · There we go. That's our vision model. So it's a small VLM vision transformer. Now we don't need that but this is going to count the parameters in our model. So we have total parameters trainable frozen.

### Freezing the vision encoder in our model

**45:30** · Now before freezing we're going to count. Now we can freeze the vision encoder by going for param in model vision model.parameters. So that's going to access that param.requires gradient.

**45:42** · We're not going to update its gradients.

**45:43** · So this is just a bull could be true. I think it defaults to true right but then we go false right so that means during training don't update the vision encoders patterns we run that boom look at that

**45:58** · so total pattern uh parameters we have 500 million right in years gone by that would be a huge model but in today's world it's I'm classifying that as small and probably in 3 years this will also be um this will be even smaller now params trainable 420 20 million and frozen 86.5 million. So that's our vision encoder is frozen. The next step towards training. So we've frozen our model. We're following the recipe of the small dockling paper.

**46:28** · Um creating a data collider. So what is a data collider? It essentially turns your so machine learning models or Nvidia GPUs work best on batches of samples or so say for example we have 128 GB of memory on the DJX Spark which we do. We want to uh use as much of that memory as possible because GPUs love to operate on when their memory is full.

**46:53** · Not too full, right? When you have a good meal, you feel good and satisfied.

**46:57** · When you have too much food, what do you do? You feel sick and you lay down. That happens here. But a collation function stacks samples into batches. So when we performed inference before, inference is another word for predicting. We did it one by one. But training is usually best done in batches. So, we're not going to make a batch size too large. With uh vision models in the past, you could have a batch size of 128. And depending on your hardware, you can actually increase that. And I'm just pulling these numbers out of anywhere. You can use whatever batch size you want, but generally they'll be in multiples of eight.

**47:28** · Um there's a funny tweet if you Google uh friends don't let friends train with batch size of over 32, but that's that's pretty old now. You can train with a much larger batch size, but because our model is so big, we're not actually going to do that. Data collider compiles things into batches. So tenses.

### Discussing batch sizes

**47:48** · This helper function which I borrowed here from the Gemma docs. So thank you very much to the Gemma team. Convert message to list of images. So this is going to go through a list of messages, the format that we created before and stack the images into a list. Uh, and then we're going to have our collate function which creates empty lists of text and images and then puts them in a batch format through the processor and then returns um those in a batch input.

**48:15** · And then we also do some masking here.

**48:17** · So we're going to mask our image token ID which is uh remember that placeholder before? We don't want our model to recognize that image token ID. We want it to recognize the pixel values. And the pixel values are that tensor we saw before. As I said, that image token that with the little brackets like that is a placeholder. That's just saying to our model, hey, an image is coming in here, but we don't want you to focus on it. We want you to focus on the actual pixel values. And then we want you to based on those pixel values and the token inputs, we want to output the um tokens that we've given it.

**48:50** · So, we're going to run that. So, yeah, there's the token ID that small VLM2 uses for the image token ID. We mask this token as it is only a placeholder in our sequence of tokens.

**49:02** · So up next we have two things. We have SFT config and SFT trainer. Remember how I said we're doing supervised finetuning which is we provide inputs, examples of inputs, examples of outputs and our model bridges the gap. SFT config is all the settings. So these are hyperparameters. Now most of these hyperparameters are either the default from the documentation of hugging face.

### Setting up SFTConfig

**49:25** · This is from TRL transformers re reinforcement learning. I've left links here to the docs. Of course, your extension is to read through all of this. There is many of them. Don't worry if you don't understand them all, but reading them is a very helpful exercise.

**49:40** · Um, and the same thing for trainer which is built on transformers trainer. But this is part of TRL. Um, so uh if we go to the small dockling paper, this is what I talked about the learning rate.

**49:52** · Let me just go to here. Learning rate, they started it off there. 2 \* 10 -4 AdamW optimizer. We can remember three things. Let's do it.

**50:02** · Gradient clipping 1.0 and warm-up ratio of 0.03. We can remember four things.

**50:08** · So, warm-up ratio 0.03, grad norm gradient clipping 1.0, learning rate 2 to the power of -4 or 10^ the4. Um, and then we have the optimizer AdamW torch fused. So, I'm going to output it to this. I've appended video here, but um for the production version or for the demo version that I'm I'm going to link, I didn't have that video tag, but I'm just putting this here so you know that this training was done during this video. Um number of training epochs.

**50:39** · Again, I've only put this at one. You could put that at four. I found four to work for this particular data set, but one cuz I'm I want to make this quite fast. Per device batch size. So, I have quite a large GPU memory. If you find you're running into errors, you may have to lower these to two or even one, right? If your GPU is 16 GB, um you may only be able to fit one on there. But try with two. If four doesn't work, try with two. And then if two doesn't work, try with one. I'm going to stay with four and then I'll let you read through um the rest of these settings here.

**51:11** · So, we'll run through that.

**51:16** · Oh no, we may have run into I've had some disconnection is issues lately.

**51:30** · 5 4 3 2 1. Elephant elephant elephant unp Okay. Uh we had to reset the Spark. I'm not sure if it's a connection issue.

**51:41** · I've had that quite a bit today actually. I'm not sure if my internet cuz again we are connected via SSH so we're doing it via Wi-Fi. Uh, I may have to look into a direct connection in the future, but we were up to creating our SFT config. Beautiful. And now we can train the model with FS SF.

**52:01** · This is a mouthful whenever you say it a lot of times. SFT trainer. So these are the settings of how to train our model.

### Training our model with SFTTrainer

**52:09** · This is what our model should train on.

**52:12** · Now you'll notice that we have the training data set here. We could train on all the samples.

**52:18** · If we do that, we can go on a thousand as well. Let's just remind ourselves of len train data set. How many samples do we have and the validation data set?

**52:27** · There we go. We got 1,200 training samples, 300 evaluation samples. I've minimized these uh 50 and 10 to make things faster. If you, as I said, I've also minimized the number of epochs. Um the model I have on my hugging face, this was trained for four epochs on all of the data. So it took about an hour or just over an hour. Whereas we're going to run this here on only 50 samples for training and 10 samples for validation.

**53:01** · And we're going to pass it in our collection function. Remember that's just going to go through the train data set, turn everything into batches, and there's our pre-processor class, uh, which is, of course, processor. This tells, um, our model how to process things like the image. Um, and it's got a big list of what all the tokens are, but or the special tokens, sorry, but we're not going to go through all that.

**53:23** · If you'd like to look through that, please do. So, let's train or fine-tune our own VLM together.

**53:32** · Now this might take a minute or so to get started and then should be about a minute or two to train. Remember this is on a vastly reduced data set about 20x less samples than are actually in. So um yeah we've reduced the time now in the full training run. Uh this is what I did was epoch 4 and then there's the time.

**53:52** · Yeah about an hour and a half or so. So there we go. We're already about a third of the way through.

**53:58** · Should be quite quick.

**54:00** · That is one of the things you uh as a machine learning engineer have to figure out is what should you do during the training time. Personally, I like to do star jumps.

### Model training starts

**54:15** · Ah got about 20 or so done and we are back. Beautiful.

### Model training finishes

**54:22** · So we get some outputs here. Training loss ideally that would go down. The loss value is how wrong your model is.

**54:29** · And the validation loss ideally that would go down to zero means your model is perfectly predicting inputs or sorry outputs from the inputs. Now I would always be skeptical if the loss goes down to complete zero. There may be some data leakage somewhere. Number of tokens. This is how much our uh or how many samples our model has seen. So remember our model is going to or our pre-processor is going to turn all of our inputs into tokens and our models love looking at tokens not images and text. Then mean token accuracy.

**54:59** · This is the raw accuracy value. 100 would mean that our model is predicting um the output tokens uh 100% of the time. And so we can get pretty high mean token accuracy over here. But again these are just numbers. Ideally the loss goes down. If that if it does, that's good. And we can see here in a longer training run, it actually did go down.

**55:25** · But uh where do the best evaluations happen? They happen when you look at actual samples, which we're going to do shortly. So we can save the model to file.

**55:36** · And then if we come over here, we should get there. We go checkpoint. That's our checkpoint that was saved during training. But these are all the files here that we've saved to file with trainer.save.

**55:49** · Now if we have a look at the files and versions of the original model right small VLM video instruct what do we have here models.ssafeet tenses and then a bunch of config files in JSON that's exactly what we get here so of course our model.safetenses safe tenses has now been upload uploaded or sorry updated to

**56:10** · our data and if we have a look at the loss curves right we see that during training the loss goes down this is exactly what we want that is the beautiful direction of a loss curve down over time now we can upload the fine-tune model to the hugging face hub if you're running locally you'll have to log in um via hf login I've left some links to do that there if you're running in Google Collab. So if we go to Collab, you will have to let me just show you here.

### Inspecting our model's loss curves

**56:39** · So small VLM2 playground, this is where I was testing small VLM2.

**56:50** · Uh you'll have to set up your HF token over there. So um I'll show you there's a guide on setup on learnhingface.com.

**56:59** · You can set up your token for Google Collab. So, we go down here. I'm going to remove the checkpoints that are in here. You don't necessarily have to do that. That's optional. Just be careful running rmrf. And so, if we refresh this, we should Yeah, now we've got a clean model file. I'm going to upload this whole directory to hugging face.

### Uploading our trained model to Hugging Face

**57:21** · So, if we go run this, this is from hugging face hub. We create a repo. The repo ID is going to be this.

**57:31** · Notice I've put the video tag there so that you know that this model was created from the video and then we're going to go API upload folder and it's going to upload this folder here and then we can see there that will of course depend on your internet speed but if we go to um this is the one I did in a previous like all good cooking shows in a previous example but that's the one we trained for longer remember for epochs. So if we see Is this the video version? Yeah, video.

**58:03** · There we go. Okay, so that's been uploaded just now about two hours ago.

**58:09** · Um, this is still going.

**58:12** · So, we'll just wait a few seconds to let this upload and then I'll show you the new version and see if it's uh refreshed on hugging face.

### Model uploading to Hugging Face begins

**58:23** · 5 4 3 2 1. Beautiful. We get a commit URL there. Now, let's go back to here.

### Model uploading finishes

**58:29** · Has this been updated? There we go. Less than a minute ago. And so the beautiful thing about uploading to Hugging Face is that there's a a wonderful data layer and that is called Zet Z. Um, and it will only actually update things that have changed. So if any files haven't changed locally, so all of these template files actually haven't changed locally. The file that did change was the model.safe tenses cuz we trained it.

**58:55** · So that's a beautiful thing about using the uh hugging face hub is that there's a incredible data layer. So if we updated our data um set in the future, right? If we added a thousand more samples um to food vision extract 3K or this particular one, it would only change the samples that actually changed. Or if we went in and edited this one and said, "Oh, this is actually this could be a little bit better. We might update these." It will only change that row when you commit it. So that's a real cool feature.

**59:25** · Now that's up uploaded. Let's delete the model and trainer and we'll empty our cage. We're going to test the fine-tune model against the base model. Remember metrics symmetrics. Always test data or test models on your custom data. So these metrics, they look good, but how does the actual output of our model look? So um use the model. So, if we wanted to use our training checkpoint model, this one, the video, remember that was only trained for about a minute or so, we could just put training args.output dur.

### Comparing the base model to the fine-tuned model

**59:58** · And I'll just show you what that looks like. Wonderful. But as all good cooking shows, I prepared one earlier. So, I'm going to use the one on my profile. And then the base model, of course, is going to be the hugging face um small VLM2500 mil. That's going to be we're going to compare the base to the fine-tuned version. So, we're going to create two pipelines. PT pipeline is stands for pre-trained pipeline. That's our base model. We got the model ID there. The FT pipeline is going to be the fine-tune pipeline.

**1:00:27** · So, we're going to load the checkpoint uh durame there, which is the model on my hugging face, which is this one here. So, let's load that.

**1:00:40** · It's going to load two pipelines. So, two models are going to be put into memory.

**1:00:47** · And up next, we're going to pick a random sample from the validation set.

**1:00:50** · And this is some random code to or sorry, random selection code from the validation set. And then we're going to inference with both models. So we'll inference with the pre-trained model and we'll inference with the fine-tune model and we'll compare the outputs.

**1:01:05** · So there we go, ladies and gentlemen. We have fine-tuned a VLM. This is the expect example model input. We've got the image. This is the uh ideal output.

### Viewing our fine-tuned model's first predictions

**1:01:16** · So, egg drop soup, food items, broth, chicken chopped, mushroom, egg whites, shredded chili chili flakes. So, that's that's a pretty good label, right?

**1:01:25** · That's from Quen 3 VL8B, which is 16 times larger than our model.

**1:01:31** · This is the pre-trained model. So, the base model, we get an empty list as we've seen before. But now, generated output text from our fine-tune model. is food one image title soup food items red chili soft shell crab shrimp daon radish shelots is it perfect no but is it in

**1:01:49** · the exact format that we want yes is it fairly close to what we want yes now remember this is only with a thousand samples uh thousand training samples real production models are often trained on as we saw small dockling was on 27 million samples so that would probably be one of our extensions is to upgrade our data set This is a data set that I made in a couple of hours the other day.

**1:02:12** · So now I know that it works. My next step would be to um really scale this up. So I've only used a thousand food images or thereabouts and 500 not food images. So in my head I'm starting to think how can I turn this into 10,000 food images and 2,000 not food images or even more. So we go back. That's the law of scaling. So the good news is our model is working right. our fine-tune VLM and optional training stage two. So, you can unfreeze the vision encoder.

**1:02:43** · You'll have to create a new uh config /trainer because there's some do um new settings um for stage two, but I'll leave that as an extension. And then you can inference there with the stage two pipeline. Because our data set is so small, um I tried this out. The improvements aren't that great. If we had a larger data set, I would assume that the data's um the stage two pipeline might actually improve a little bit more. Now, next, of course, you and I can check our model's performance with code.

**1:03:12** · But what if we wanted to share our model with someone else uh in an easily interactable fashion? That's where we can create a demo with Gradio. We're going to need three files: app.py, requirements.txt, and readme. So, we'll make a directory for our demo.

**1:03:30** · So if we go over here, this will be demos here. Food extract vision number one. And then we can write a file here.

### Creating a demo with Gradio

**1:03:39** · This is app.py.

**1:03:40** · So gradio, the whole premise of gradio is we're going to define our models here. These are just what we did original pipeline. So that's the base model pipeline.

**1:03:50** · And then we have the fine-tune pipeline.

**1:03:52** · We have a helper function to create an input format. Because grad is going to take an image, we need to format that into a message. And then we can pass that to our model just like we've done before. We're going to give uh our model a GPU to run on. That's what you can do in hugging face spaces. So let me just go hugging face spaces.

**1:04:11** · So these are all demo apps, but you can also create your own app. You can do it through this is an app through the web interface, but because we're programmers, we're going to use um the code code to do this. Uh, you can also use zero GPU, right? Um, I'm a pro hugging face subscriber, so I get a little bit more access to the zero GPU, but I believe this is also free. Um, correct me if I'm wrong. And then we could upload some code via that, but we're going to do it through here.

**1:04:40** · So, this is just our function that Gradio works off. Input function output. So, it's going to pass in the input image.

**1:04:49** · It's going to get the outputs from the original pipeline and then it's going to get the outputs from the fine-tune pipeline and return both of those. This is some title uh and demo description written in markdown and then we create our grado interface. So here's our function extract foods from image inputs title description outputs and then we have some examples as well. So I'm going to write that there to file that's going to go into there. Um, so we got demos.

**1:05:17** · Oh, excuse me. Demos food vision extract app.py.

**1:05:22** · All right. Beautiful. And then we have a readme which is going to right there.

**1:05:27** · Say I'm going to put this here. Note this readme was authored in a live tutorial recorded for YouTube.

**1:05:42** · Link coming soon.

**1:05:44** · All right, we'll save that there. That's going to save to readme.md over here. There we go. Beautiful. And then we have our requirements. So, one requirement you might not be familiar with, um, all of these transformers, torch, accelerate, uh, gradio, torch vision is numb to words. That's a requirement that I found out was required for small VLM2. So, um, excuse me. You might have to install that if you're running Google Collab, but I'm sure you would have found that out by now. Finally, we can upload the demo to the hugging face hub. We can create um uh some details about the parameters.

**1:06:17** · We can also create a space repo here. So the repo type HF repo type is going to be space. We're going to use the gradio SDK. Then we're going to get the full repo name. And then we're going to upload our whole demo folder using this.

**1:06:34** · So uploading food extract vision demo app.py from YouTube tutorial video.

**1:06:42** · So, we'll run that and it's going to, as I said, wrap this folder up and then if it all worked, we should be able to go to hugging face food extract. Okay, so it's going to be rebuilding because we just uploaded it and changed it. But we got our files here. There we go. Less than a minute ago. So, you know that this is a real live cooking show. And then we go to read me. Does it have a little note? Note, this readme was authored in a live tutorial recorded for YouTube.

### Uploading our demo to the Hugging Face Hub

**1:07:09** · Of course, the link I don't have yet, but I will have once this video or once you're watching this video. So, we'll wait for the app to rebuild. But that, my friends, is officially um fine-tuning a VLM. We did it all locally in about an hour or so. Uh but of course, it took some time to prepare the data set. And I've got some live streams if you want to see what's going on there. So, food extract vision. This is the prompt we feed our model. Uh, do we have is this usable? Let's try it.

### Trying out our demo

**1:07:39** · There we go. What about this? So, this is going to be one of the things that we need to fix in a future model. If you'd like to see that, please let me know.

**1:07:52** · Our fine-tuned model tends to output repeated Yeah.

**1:07:59** · So, that is one of our extensions. How do we fix that? And then if we go here, beautiful French fries. So try it with your own images. The link will be in the description if you want to try this out.

**1:08:09** · You might actually also have your own version.

**1:08:12** · But if we go to the keynote, I have some extensions slash extracurriculum for those who want to keep going. And actually these are some things that I would personally try myself. So formalize evaluations. So we've gone from base model, fine-tuned it on a custom data set to a demo that people can use. And we've noticed that our fine-tune VLM performs okay, much better than the base model, but not as good as what we'd want.

### What's next and extensions

**1:08:38** · Uh, so if we wanted to formalize this and get it towards production, we definitely have to formalize some evaluations. So we could write some evaluation code to take the outputs from our fine-tuned small VLM model and compare them directly to the Quenval 8B. So we've kind of vibe avoued our model as of now. Number two, we could improve the data sampling both in volume and in diversity.

**1:09:00** · So if we find out that our model makes mistakes, yes, it's already overgenerating things, yes, it doesn't uh for some images doesn't extract the right foods, um etc., etc., we could improve the input data. So mo most of this is more samples and more diverse samples. For example, we could introduce 1,00 plus real life photos of food uh on top of the food 101. So, Food 101 data set is a public data set. Um, but the images aren't all that high quality.

**1:09:30** · Whereas, if we wanted to optimize our model for extracting foods from plates of food, just like we saw in the Neutrifi demo at the start of the video, we would definitely want to incorporate samples like that in in what's the what's the terminology? I think it's Genensi Gumbatu, which is Toyota's thing. Real real testing, real locations. If you want your model to improve, the better or the more real your data is, the better it'll probably be. Um, remove the input prompt. So, right now, our model is fine-tuned with text and image pairs.

**1:10:00** · In the future, we could potentially just remove that input prompt and go straight from image to text. That would save us on input tokens. We wouldn't have to input that prompt. So, let me show you here.

**1:10:13** · What I mean by this is this prompt. We have to input this text to our model cuz that's what it's been fine- tuned on.

**1:10:19** · Now, if we wanted to save on some input tokens, what's this token counter?

**1:10:24** · Because why would we want to save on that? The less tokens that we need, that's 160 tokens. Now, this is using GPT5 tokenizer, but it's going to be about the same for small VLM. That means we don't have to infer on those 160 tokens, which is going to potentially improve latency.

**1:10:43** · Um, finally, so, oh yeah, if we remove the input prompt, we would just go from image to structured output. Uh, number four, we've already spoken about this, but fix the repetitive generation. I think we'd have to uh either train it on more data or in supervised finetuning or introduce reinforcement learning for um avoiding repetitive generation. And so what I would do for that is have a um it's called RLVR. So reinforcement learning for verified rewards. I would have a reward function for our model to uh generate the right amount of JSON.

**1:11:14** · Um so not not repeating things. That's what the reward function would be. If it if it generated a non-repetitive output, it would get a plus one. If it generated a um a repetitive output, it would get a zero. So that's RL or an RL technique.

**1:11:33** · There's a lot more to it than that. Uh or we could go a lot deeper than that if we wanted to. Finally, we would try the fine-tune process on another data set.

**1:11:41** · So, right now we've done food extract, but my challenge to you is practice fine-tuning a small model for another structured data task such as uh extracting details from an invoice like we saw with um Gemini. So, take an invoice, extract details such as title, date, amount, description, etc. Or you could replicate a feature like Apple's visual intelligence to rip an event from a poster. So you would get the date, the event title, um, and then format that into JSON. So you could put that straight into a calendar. That would be a great way to practice fine-tuning a VLM.

**1:12:13** · So uh, I believe the model has likely seen many more of samples like this. So extracting text from images, so it's likely going to be better at that task.

**1:12:24** · So that's me fine-tuning a VLM. If you have any questions, please leave them below. There's also another video on fine-tuning an LLM. Um, if you want to fine-tune an LLM for text only, go and check that one out. But if you'd like to see anything else in the future, please leave a comment.