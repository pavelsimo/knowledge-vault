---
title: "Getting Started with CUDA and Parallel Programming | NVIDIA GTC 2025 Session"
source: "https://www.youtube.com/watch?v=GmNkYayuaA4"
author:
  - "[[NVIDIA Developer]]"
published: 2025-04-10
created: 2026-07-06
description: "Join one of CUDA's architects on a journey through the concepts of parallel programming: how it works, why it works, why it's not working when you think it should be working, and in particular why it'"
tags:
  - "clippings"
---
![](https://www.youtube.com/watch?v=GmNkYayuaA4)

Join one of CUDA's architects on a journey through the concepts of parallel programming: how it works, why it works, why it's not working when you think it should be working, and in particular why it's different on a GPU from a CPU.  
  
We'll look at different approaches to parallel programming in CUDA and how to take advantage of the hardware it runs on. This is the next episode in what has become a series looking at the way that CUDA and the GPU work, and why they work this way. This session will focus on how to think about parallel programming on a massively-parallel GPU and why that might be different to what you're used to. If you've never even written a parallel algorithm then you'll learn all sorts of new things, but even if you're a ninja you'll walk away with some new tricks up your sleeve.  
  
Speaker: Stephen Jones, CUDA Architect, NVIDIA  
  
Key Takeaways:  
▫️Introduction to parallel algorithms  
▫️Hardware and even software design is running up against the laws of physics, which will change computing in a fundamental way  
▫️How parallel programming on a GPU is different to what you might be used to  
▫️Techniques for getting the most out of CUDA  
  
CUDA Toolkit: https://developer.nvidia.com/cuda-toolkit  
  
Watch more NVIDIA GTC sessions on demand: https://www.nvidia.com/en-us/on-demand/?ncid=so-yout-194474-vt33  
  
Topic: CUDA Development and Optimization - Programming Languages / Compilers  
Level: Technical - Beginner  
Replay of NVIDIA GTC 2025 Session ID: S72897  
  
  
  
  
  
  
  
  
#CUDA #NVIDIA #gpucomputing #parallelcomputing #parallelprogramming

## Transcript

**0:07** · Hello folks, thank you for sticking around for the last session on a Thursday. Well, we have more sessions tomorrow as well, so hopefully you'll be in to see some of them as well. I'm Stephen Jones, as my hype man Fred was telling you, and I'm one of the CUDA architects.

**0:26** · So I spend basically all my time thinking about CUDA. I've been working with CUDA since 2008, and I've been doing this series of talks over the last four or five years on how to write CUDA programs and how pro CUDA programming works. I'm never going to teach you in 45 minutes how to do parallel programming. That's not something you should bother trying to do in this kind of time frame. What I try to do is set a mental model about how the GPU works and have you think about how I think about how it works.

**0:55** · A lot of the way we build CUDA is that, as the hardware architects develop new things, we think about how this can be portrayed in a meaningful way in a programming language that's intuitive and makes sense to people. So sharing what's in my head in terms of how I think things work will hopefully help you get a sense of how CUDA works.

**1:18** · Well, this particular one is about parallel programming, which is a particularly hard topic. I'm going to start easy; it will get a little bit technical, but really fundamentally, the truth is that parallel programming is hard. So fundamentally, don't do it. It's way easier not to do it. You really don't need to do it very much. As a member of the video team, I get access to Jensen's lovely keynote slides. This is from one of his keynotes. All those Christmas tree things are these dependencies that his artists drew of all the different packages we've got.

**1:48** · Every one of those green dots is one of the hundreds and hundreds of packages that NVIDIA has, and really, parallel programming is only right there, and none of the others really need parallel programming at all. So you really don't need to do any parallel programming.

**2:11** · Because we're all programmers and we're all fundamentally lazy, for every 10 lines of code you write, you get a bug. You shouldn't do parallel programming. But CUDA builds this entire stack of things to help you not do parallel programming. This is the secret of CUDA, which I put on the top of the slide today because it was something I was saying to someone just the other day. The secret of CUDA is that it's not just one thing; it's all of these things. There are these levels of abstraction that break down who's responsible for doing what in the application. Of all these layers, there's way more stuff at the top than at the bottom.

**2:44** · There are hundreds of SDKs and only a handful of compilers. There's really only one layer where parallel programming is actually needed, and that's when you're writing a GPU kernel. We'll talk a bit about that, but largely, we're not going to talk about that. We're going to talk about how to avoid writing a GPU kernel. There's a little bit of parallelism that you need a bit higher up the device, and it's a different kind of parallelism. I'll get to that as well. It's much more interesting because it's much easier to do. But largely speaking, there's a lot you can do without any parallel programming at all, and that's probably the first thing to do. I kind of liked the subtitle as well.

**3:16** · There's actually a lot less parallelism to CUDA than you think. So I thought, you know, I'll just make a slide of "CUDA: A Lot Less Parallel Programming Than You Might Think."

**3:30** · And that's good because it's hard, right? You should try to avoid it. To help you avoid it, CUDA has built this giant array of different things. I had this slide in a previous talk a couple of days ago, and this is obviously just a tiny fraction of the things that are GPU-enabled. The point is, all of these things exist. It's a little corner of the CUDA platform stack, but they all exist because you're much better off at the top than you are at the bottom. That line that I drew, "No Parallel Programming Needed," is the vast majority of these things, and it's very productive to use.

**3:59** · Parallel programming is hard and annoying and difficult to debug, and calling someone's framework, which just does it magically for you and they've done the debugging problem for you, is much better.

**4:13** · Somewhere down below is dragons, and it's very complicated, and we don't really want to go there. We'll touch on it, but largely speaking, you don't have to do much because, if you think about programming, you've got a bunch of boring stuff that we all have to do, and AI code assistants are hopefully going to change all of that for us. Then I had one write some unit tests for me the other day, and it actually came out with sensible, reasonable unit tests.

**4:38** · So I'm hopeful that the boring stuff, like config file management and those types of things, can all be farmed off pretty soon—not to interns (apologies to anyone who was once my intern), but to coding bots instead, and give the interns something more interesting to do.

**4:56** · The code that you actually have to think about is probably less than half, and of that less than half, the majority of it is the stuff that your program needs to do, like memory management, communication stuff, sockets, and all the rest of it. The actual stuff that could be parallelized is just a fraction of that, and of the stuff that could be parallelized, the overwhelming majority of it is probably algorithms that someone has already done for you. So, really, if you like, honestly, if even 1% of your code is actually stuff you need to write parallel programming for, then you mostly should be paying attention to the other 99%.

**5:30** · That 1% is still important, but it's not where the bulk of what you get done, and the performance gains you're going to get and the productivity gains you're going to get, are going to live.

**5:46** · A place that you often start is at the very top, right? These frameworks and I've thrown a few different things on the screen here—some AI frameworks, some graphics ones, some computational physics ones. What they do is they take you into their embrace and help you build an application usually in a very specific domain. Whether you're making AI networks with PyTorch or doing molecular dynamics with something like LAMMPS, or graphics effects with Houdini, all of these things put you in the shell.

**6:19** · They provide you with ways to program much more efficiently, and you get way more done. They're very productive, they are much easier to think about, and they almost never show you parallel programming. They're all GPU accelerated, and at this point, hundreds and hundreds of things are GPU accelerated. So you actually have a lot of choice, which is fantastic. If the framework doesn't quite cut it for you because you're making your own bespoke application in some way, then almost certainly the majority of what you need is going to be available in CUDA's math libraries. This is some of the low-level libraries. There's a whole array and stack of hundreds and hundreds of these things.

**6:54** · The low-level libraries are really the core functionality, the building blocks if you like, that you'll build things with. So cuBLAS is for linear algebra, cuFFT is for your transforms, random numbers, different operations, and so on. There's a whole family of these different things, but the math libraries are your mainstay. These libraries have been tuned by NVIDIA Ninjas over years. You would spend years to write a program that came close to what these things will do, and why would you? You've got better things to do with your years of work. And if you do write a program that beats these, you should definitely talk to me because I will hire you.

**7:26** · The people writing these are now way better than me. My first job at NVIDIA was writing the FFT library, and the people who do it now are just so much better at it. Use the libraries, and I say this every time because I talk a lot about programming CUDA, and the answer is that these are the things you should never even try to match. But if you have to go somewhere that the libraries don't go—because not everything is a pre-baked linear algebra function in cuBLAS—there are, of course, programming languages which still isn't CUDA and still isn't a thing you have to get to.

**7:59** · I mean, some of it is CUDA, but these are things from the CPU. When you string your operations together, these languages, packages, and constructs allow you to formulate parallel code without ever having to invoke a GPU compiler. So I'm giving you all the reasons and ways that you're not going to be doing any CUDA programming because I think parallel programming is hard and a big waste of your time unless you really, really have to do it. Speaking of time, here's actually a chart that I used to show the interns.

**8:34** · You kind of think ideally that you know you're going to put in some effort and it'll get better. If you do two weeks, it's twice as good as one week, and you get to the end. Then you go and look up something like PyTorch, and you think, "Oh, it's going to be amazing; it's going to give me peak performance instantly with no effort." But the real world is a little bit more realistic. You're going to gradually improve, go through a phase of goodness, and then it'll kind of curve off. The truth of the matter is actually much messier, and we spend a lot of our time frustrated and banging our head against the table.

**9:09** · In fact, the very end thing you end up doing is hiring an intern because the interns are just so brilliant about these things. I see some of my old interns laughing in the audience, but this is really our experience programming. But back to the slightly more realistic curve, the goal of all of us, and the reason I start telling you about parallel programming by telling you about not parallel programming, is because what you want is to shift this curve to the left. You want results fast, you want good enough results with less effort, and you really don't want to waste your time on that long tail at the end of just tuning.

**9:42** · It's the 80/20 rule: the last 20% takes 80% of the effort. So you can draw these curves of different types of things. The frameworks get you not zero time to success, but they ramp up pretty quickly. They may not get to the same peak as some ninja-tuned NVIDIA library, and you can probably hand-code your kernels to be even better than that if you're going to get a job from me. But largely, you want to be on the left-hand side of this picture, except for the one or two cases that really matter.

**10:19** · But I promise to tell you how to write a CUDA program. So, first, you write it by not writing CUDA, but I will tell you about some of the CUDA as well. I realize I should keep an eye on time because I do have 98 slides today. This is like the OG example of CUDA. This is the very first example that Ian Buck wrote up to tell people how the hell CUDA works. It's implementing the single-precision AX plus Y routine. It's a routine that's very important in matrix multiplication and has been in every library for the longest time.

**10:58** · It's the most useless benchmark for benchmarking any machine ever. When anyone shows you performance for this, you immediately ignore them because it's purely just a memory benchmark. What you do is you have a function, and it takes a couple of floating-point arrays, x and y. Then they multiply x by a and add it to y, and that's the result. In a normal CPU program, these things serially go through a big for loop and calculate the whole array. This is how the CPU has always worked.

**11:25** · For the GPU, the way CUDA would change this is to say, instead of that for loop, if I've got, let's say, a million elements down there on the left-hand side, so a million elements in CUDA, what you do is you launch a million threads. So instead of having a sequential for loop, you have a parallel grid launch. The grid is launched in two different dimensions. I'll tell you a bit about that in a moment. I think many of you know this as well. We're going to start easy and get harder.

**12:00** · What this does is launch a thousand blocks with a thousand threads. The result is that all of those thousand threads instantaneously calculate things, and you're much better off. This is the essence of where GPU performance comes from. It's this massive parallelism. The way it actually runs is that the GPU itself, like a multi-core CPU or pretty much any processing device, has lots of different processor cores we call streaming multiprocessors (SMs). So this universe of a million threads that I need actually gets broken up into what we call thread blocks.

**12:30** · The thread blocks then get mapped onto the GPU. I've got a picture of a very old GPU from 2012 here because we only had 15 SMs back then. But largely, what happens is each one of these yellow things is an SM, one of the streaming multiprocessors for the GPU. What happens is these different blocks land and run on these different SMs, which are just the processing cores. Each SM itself has 2,048 threads inside of it.

**12:57** · By breaking my work up into these blocks, just like you would on a multi-core CPU, you're able to exploit the natural parallelism built into the hardware. Because 2,048 threads are allowed in the block, you can actually fit two blocks of my 1,024-thread size program on a single SM. So my 15 SMs could run 30 blocks of my program here.

**13:25** · I use this old GPU because, even though it's got 15 SMs and that's way fewer than the 1,024 blocks we've got, when I look at one of the more modern GPUs, like Hopper, we don't have a picture like this for Hopper, otherwise, I'd have shown you Hopper. Hopper has 132 SMs, which is still way fewer than a thousand blocks. So a key element, and if you've seen any of these talks before, you know I always point this out, is over-subscription. You want to give the GPU more stuff than it knows what to do with. More stuff than it will fit on it at any given time.

**13:56** · That's because the way the GPU runs these things is it will fill the SMs with all the blocks it can find, and then as one block leaves, another block enters. So the amount of time that your GPU is idle is very small.There are 132 SMs on this Hopper device, and that means that when one block leaves, less than 1% of my GPU falls idle. By having a deep pipeline of many of these blocks, the total throughput is much smoother and cleaner. It's also a great way to scale. We had 15 SMs 10 years before Hopper on Kepler.

**14:40** · With effectively 10 times the number of SMs, Hopper naturally just instantly runs nine times more stuff. That's because I have a lot of blocks.

**14:54** · If I only had a few blocks, it would never have filled Hopper. By over-subscribing my machine, I scaled pretty nicely over 10 years. A subtle point, though: I showed you a million data points here, and I launched a million threads to process them. I kind of correlated threads with data there, and that's actually not true. I lied to you about that. We broke up our million threads into 1,024 blocks of 1,024 threads each. That's what the arrows were showing.

**15:20** · But because threads and data are not the same thing, we ended up with a million threads for our million elements of data. However, my Hopper device only has a quarter of a million threads. A quarter of a million threads is a lot of threads, but it's still way fewer than the total number of threads I need. Hence, the streaming of those blocks. But even though I can stream the blocks through, this isn't the only way to divide my work. I don't have to do a one-to-one mapping.

**15:52** · In fact, there are real benefits to not doing one-to-one. The fact that this requires a million threads, with one element per thread, can be structured in my program. That indexing thing I highlighted is where I say, "What is my thread ID? I'm going to index my data according to my thread ID." So I've launched a million threads. If I'm numbered 1,000, I'm going to get data element 1,000. I didn't have to do a one-to-one mapping. I could have said, "Let's do four. Let's multiply my index by four, so each thread is going to take four elements of data." Then I'll do i + 1, i + 2, and i + 3.

**16:32** · This is just very basic CUDA C++ code, and now each thread is doing multiple things.

**16:37** · I now have a quarter of the number of blocks. First, I have to be a little bit careful because if my threads don't divide perfectly, I have to have a little if case in there to make sure I haven't read out of bounds. Then, finally, I have to update my launch. Instead of launching 1,024 blocks, I launch one quarter of that because I'm now doing four elements per thread. So I've got to do a few adjustments. It doesn't happen automatically; it's actually something very difficult for a compiler to do for you. These are the kind of transforms you have to think about when you're designing your code up front. The result is that now I can fit almost perfectly on the machine. There are a lot of benefits to doing this.

**17:09** · Not only am I fitting on the machine and launching fewer blocks with less overhead, but I'm actually batching my memory loads and reducing the amount of jitter. There are a whole bunch of reasons why, on my laptop, this runs twice as fast. There's a lot more you can do in what looks like a very simple kernel to actually boost performance significantly. I've got an example from my colleague Mark Harris, who many years ago did something about reductions. I'll show you something of that later, where he demonstrated sequences of optimizations you can make.

**17:44** · I'm not going to go through those types of things here because they're already out in papers and presentations. But the point I want to make is that the way we've designed the GPU is built with this exact thing in mind. The idea is that you've got lots of blocks, more blocks than you can fit, and more threads than you can possibly fit. We give you a lot of choices about how to slice and dice them. As each architecture evolves, and as Moore's law compresses the transistors to be smaller, we can fit more SMs onto a piece of silicon.

**18:17** · But notice that while the SM count goes up, which is the core count, the number of threads per SM does not go up. The reason the number of threads per SM does not go up is that changing the width of my program is a significant structural change to my program. You saw even just changing from one element per thread to four elements per thread involved touching my program in three different places.

**18:38** · While we could just say, "Well, build one giant SM across the whole machine," that's actually bad in terms of future-proofing because then the next machine getting bigger forces you to go back and change your code all over the place. We care a lot about the fact that your old code runs on new hardware. But not only that, if you had a large number of threads, every time you need to synchronize your threads, you've now got to communicate all across the GPU. There are very good reasons to keep things to a reasonable size. 2,048 threads for the last 15 or 13 years has been the choice we have made.

**19:15** · Locking in that, increasing the SM count, and streaming with too many blocks is really the way that GPU programming scales. As you think about your parallel programming, you're trying to fit inside these bounding boxes of a large number of independent blocks with a fixed number of threads. Now we get to the dragons. Underneath these dragons, I pointed out before, there's an area of parallel programming: the kernel authoring area. We're going to start there and go a little bit further up over time, but parallel programming is needed there. I've just been showing you aspects of even a very simple AX plus Y program.

**19:53** · There are subtleties to it that can make a factor of two in performance very easily.

**19:59** · When you think about how work runs on the GPU, I showed this slide last year, and people complained at me because they said there are more than two types of parallelism, and there are many nuances to types of parallelism. But fundamentally, the way I think of these things is that I've either got independent programs. It could be the same program running in two different places, but they're totally independent programs, not interacting with each other. Or I've got one program working on lots of data, doing the same operation across lots of data. That's task parallelism versus data parallelism.

**20:28** · Everything else—whether you've got model parallelism, pipeline parallelism, weight parallelism, and all the different parallelisms that people write papers about and publish—really boils down to these two choices.

**20:44** · The thing about the GPU is that CUDA is both. We've broken our data up into independent blocks of work, and that is task parallelism. Even if I'm running the same program on all of them, the program is at a different place. Maybe the instance of the program is different because there's a block ID for everything. These things run really wholly separately. If they need to communicate data, then they have to. There's a whole different talk I could give about parallel data structures and atomics. But largely speaking, I've broken my program into independent blocks so they can make independent forward progress and run in parallel.

**21:18** · Within a block, my 1,024 threads on my SM—my maximum is actually 1,024 threads in a block—that is the data parallelism. That is where the kind of code I was showing you before comes in. The fact that we've got both of these things to make the GPU run efficiently has interesting implications for how a CUDA program works. So we'll start with the data parallelism because that's the hard stuff. When I said parallel programming is hard, this is the stuff I mean.

**21:44** · This is something if you've ever sat in a computer science course, something like a reduction, which is this operator that I'm showing you right here, is one of the first things you see because it has a quintessential property of parallel programming that's incredibly powerful. So here's my serial code for my reduction. It looks a lot like my AX plus Y code. What I'm doing is summing all the pieces together. In this picture, I've got 64 boxes, so it's going to take me 64 steps. Now, if I have a multi-core CPU, I can hand this off to different cores.

**22:18** · With a four-core CPU—today you have many more than that—but if I had a four-core CPU, I could do it serially in four different chunks and go four times the speed, approximately, with a final addition at the end. If I had a 16-core CPU, I could do even more. I can keep breaking it up. Interestingly, when you run into something like this, you get to this point where you've broken it apart so much that the second step of adding it all together cancels out some of the benefit you got from going parallel. So you do have to think about how the interaction between the separate pieces adds up, as well as the optimization you've got on the individual parallel pieces you're doing.

**22:57** · This is classic stuff for a divide and conquer kind of algorithm. So I'm dividing even more, and I conquer it faster to overcome that final addition. I can divide and conquer twice, I can keep dividing, and I can keep on conquering. This divide and conquer approach is really the essence of a lot of these core fundamental parallel algorithms. Reduction is one of them, where by doing this division and conquer—this pair-wise or it doesn't have to be pair-wise, but this repeated recursive sequence of operations to reduce things down to a single result—gives you what is a logarithmic amount of time instead of a linear amount of time.

**23:33** · This is a hugely important thing for programming in general because the time order of my algorithm tells me how, as I get more data or more work, how fast I can solve it. Matrix multiplication, for example, scales as the square of the number of things you're trying to solve. So as your matrices get bigger, it becomes unsolvable problems where doubling the amount of work only gives you 40% more compute to do that. This is really interesting because now you have a super-linear speedup on your work, or a sub-linear slowdown, depending on how you look at it.

**24:06** · This is the essence of parallel algorithms, and there are several of these core building blocks of parallelism, like sorting, prefix sum, and map.

**24:27** · These are things that, if you look up a parallel programming book, they spend a lot of time on each of these because when you write a parallel program, these are the functions that you have in your head, the toolbox you have as a programmer to take your data and approach it in a parallel way. The more you can convert the sequence of operations to these types of operators, the more you're getting out of your parallel program because it scales logarithmically instead of linearly. You really lean into the threads. Now, another key property of these is that the degree of parallelism I can bring to bear has major implications.

**25:00** · The more threads I've got, the wider a thing I can do. For a reduction, on the left-hand side, I've got enough threads for everything, and that works in logarithmic efficiency. On the right-hand side, my quad-core CPU doesn't really scale the same way. Once I run out of threads, I end up effectively serializing my chunks of parallelism again. This is why these algorithms are incredibly beneficial on the GPU because I've got a quarter of a million threads. I've got a lot of threads I can bring to bear on these algorithms, and so they become incredibly powerful.

**25:42** · In terms of this reduction, even though the code is relatively simple, I got this code from Mark Harris's paper. A basic parallel reduction is just loading up some data and doing pair-wise additions to them. He did something slightly smart and used shared memory, but I'm not going to deep dive into that. There are plenty of resources online telling you how to do reductions. The point is, the code is relatively small and compact, and I can enact this parallel reduction very efficiently on the GPU. In the same way that I could double my performance by simply reading four values per thread in my previous example, I can do even better with more complex things like reductions.

**26:17** · But suddenly, my code is full of templates, complicated switch statements, and all sorts of weird synchronizations. There are all these optimizations that happen, and his paper points out that if you do this stuff, there's a factor of 30 speedup difference between the basic and the ninja level of work. He had a few other points along the way, and he does this in seven steps. It's from 2009 or 2010, and it's a great paper because it so clearly points out the steps you can take to go from 1x to 30x.

**26:49** · If you're a ninja and you can come up with this and understand enough about the GPU and have watched all my previous talks, you can get a long way. But just imagine doing that for every single one of these operators. People write whole PhDs on ways of doing parallel sorting, and it's just crazy trying to optimize each one of these detailed pieces so you can put them all together to solve an algorithm you've got.

**27:26** · I actually used to ask in interviews for people to write an algorithm to find the unique elements in an array. I stopped asking it because it's kind of unfair. It turns out it's really hard.

**27:40** · If you understand your parallel operators, you can do it in a sequence of about five or six steps, but people would just tie themselves in knots and get very upset. So I stopped asking it.

**27:51** · The point, though, is that you don't need to write these things yourself. Data parallel programming is even harder than any other kind of parallel programming because you have to think about all these things. So you shouldn't do that either. The good news is that someone's already done it for you. In the same way that we have these math libraries for doing transforms for you, no one in their right mind should ever write a transform again, except Lucas.

**28:11** · We've got these libraries for kernel functions, which are included and put into your kernel so you can invoke a sort or a reduction or a prefix sum operator or all histograms or all these other things that are available. This is the cuBLAS library, which is part of the CUDA C++ cooperative (CCCL) library, and its Pythonic cousin, CUDA cooperative, which is the exact same thing but in Python for writing Python kernels. This year, we've really gone big on putting Python up and down the entire stack.

**28:54** · cuBLAS offers all of these operations, and it doesn't just offer them in terms of a block-wide, which is what we've been talking about here, but even sub-block things called warps or the whole device. It's very flexible, again written by ninjas who know far more about that stuff than I do or than you do, and why would you write that again? It's way in that 1% thing. Don't do the other 99%. Just work on the stuff that you need. These are basic building blocks.

**29:15** · You can literally build any parallel program with these foundational things, but don't go and build an FFT with them anyway because a lot of the math library functions for these four libraries—the linear algebra library, the transform library, random number generation, and matrix factorizations—have functions available for calling inside your program.

**29:43** · So if you need to produce random numbers or multiply some vectors together, rather than writing it yourself and going through all that disgusting, terrible, and difficult-to-debug code, just go and call one of these library functions. We put a lot of effort into making sure that, at all these different levels of abstraction, whether you're writing the low-level co-operators, invoking the libraries directly, or just launching something as a giant grid across the whole machine, there's something there to try and avoid you having to do any parallel programming.

**30:16** · Now, sometimes you can't fully avoid it. On the right-hand side, there are these things I've been talking about—this task parallelism block. If a CUDA block is a task parallel construct, a unique program running one instance of a program many times across the machine, these functions which take over my block and the threads in my block are the things they're operating on. That's the device library section, the task parallelism side of things. But it's still a library.

**30:43** · If I need something weird that cuBLAS doesn't have, like some matrix solve that hasn't existed before or some strange image processing filter that I have to write for myself, I'm still going to have to go and write that code on the left-hand side, the light green arrow. You can mix and match these.

**31:05** · It's very important when you build anything in CUDA that you can mix and match them. But really, fundamentally, while libraries can never cover everything, I need that custom code, and so can we get the best of both worlds? This is something we've been working on for quite some time to try and bridge that gap between pre-baked stuff that the ninjas have written for you and getting your hands really down and dirty with crazy warp-level template programming.

**31:38** · I think we can do something. We can get you task parallel at the kernel authoring level as well. I've been talking about this hierarchy of programming models. If you saw me talk about this a couple of days ago in a talk about what we're doing on CUDA, I showed this same picture. You've got these three levels of parallelism. You've got bulk parallelism on the left-hand side, which is how PyTorch works or anything generally works. On the far right-hand side, you've got the low-level thread stuff we've been talking about.

**32:14** · But in the middle is this task parallel programming, which is much more accessible, much easier to debug, and much easier to think about. If you can still do useful things with it, that's where the cuBLAS and the device-enabled math libraries exist.

**32:31** · So we built a programming model, or I guess we are in the process of building a programming model because you never finish building one of these things, that we call cuTile. I showed this slide a couple of days ago as well. This is tile programming for CUDA, and I'll tell you exactly what I mean by tile in a moment. This is that block-wide task parallel operation where you're not having to go all the way down and get into data parallel thread management, but you can still write very general programs. So if the library functions aren't giving you what you need, you have access to these things.

**33:04** · The granularity is an array or a tensor. You do tensor A plus tensor B equals tensor C instead of having to explode it into individual elements. It's shockingly common that many of the programs we write, whether it's image processing, linear algebra, matrix multiplication, or even the unique duplication work that interview question I used to ask and no longer do, have pretty regular chunks of data.

**33:36** · The other benefit of tensor programming is that we have a lot of tensor hardware inside the chip for accelerating some of these expensive and difficult n-squared operations. I can map tensors, or I can get a compiler to map tensors relatively easily onto things like tensor cores. So the power that you can get, in principle, if you can express your program as these data parallel tensors, you've simplified your program a lot, but you still have a general programming model.

**34:01** · I think this is exactly the gap I was looking to fill. So let's talk about tiling data. If I've got a tile programming model, I should explain to you what I mean by "tile." The same kind of granularity decisions have to be made that we made beforehand, like in my AX plus Y example.

**34:20** · In my AX plus Y example, I had this giant array of data, and I split it into a bunch of blocks. Then I figured out that I can do a lot better if I'm doing multiple elements per thread instead of one element per thread because that's generally true about how the GPU works.

**34:34** · So, in this 1D simple example, this can also apply in a similar way to how I tile my data. Remember, data and threads are not the same thing, and in this case, tiles and blocks are not the same thing. I can explode my problem into an 8 by 8 grid of tiles, sized perfectly to fit inside my cache or my shared memory or something like that. I can issue one tile per block, just like I previously issued one element per thread. It's probably not the best, but I can do it, and it's nice and easy. But I could group this in all sorts of different ways.

**35:03** · I could have a block per row, I could do eight tiles per block, so I've got a 1x8 grid now, and I'm only launching eight blocks. Or I could have a 2x8 grid and break it into different pieces, so now I've got 16 blocks.

**35:17** · I could have them square, I could have them long, I can do all sorts of different things.

**35:21** · The way you choose to break your program down depends on what you're doing. If I'm processing

**35:48** · strings, I probably want long horizontal pieces. If I'm processing sparse data, I probably want columns. If I'm processing images or something, I probably want square shapes like this. The way you break it down is a function of what your data is about and the processing you're going to do on it. There is no way that I, at the level of a CUDA compiler, can possibly know anything about your application, so I'm not going to try because I won't do as good a job as you.

**36:12** · I'm going to ask you to do the first step, the task creation step, of breaking your data down and then figuring out how to map it—like four tiles to a block, two tiles to a block, or one tile to a block, or whatever you want to do. The key part of this programming model is that you're launching a grid of blocks to process tiles, just like in regular thread programming, where you launch a grid of blocks to process threads. These are tile blocks instead of thread blocks. Because we are in task parallel mode, because we are in array-based mode, your program really only has one thread, or it looks like it has one thread.

**36:48** · Vector A plus vector B equals vector C doesn't take lots of threads to do. Under the hood, a compiler is going to sit there and understand something about your data and understand how that mapping is going to apply.

**37:04** · It's going to make all those great decisions about crazy stuff and get a factor 30 speedup that none of us really understand and don't want to learn enough about the GPU to understand. You should not be spending your time on that. If you don't have to, don't do it. Parallel programming is hard. Don't do it unless you have to. Here, you're doing some parallel programming, breaking your thing down into independent pieces. You do have to think about that, but after that, you're saying, "No, I'm just going to write at the tile level. I'm going to program at the task level." And it's going to take this for me and then figure out the mapping onto different pieces of hardware with different shared memories. Maybe one hardware wants four elements per thread, and another one wants eight elements per thread. The compiler knows all that, and we don't.

**37:38** · I don't even remember what the proper balance is for all the different GPUs we've got, so many generations of GPUs over the time I've been here. So, really, this cuTile programming is an extended CUDA where the thread-level CUDA that you're familiar with is extended to this block-wise, tile-based model.

**38:04** · I think this bridges the gap between that and the ninja-tuned libraries that you can invoke, like cuBLAS and the cuDNN libraries and so on. Tile parallel programming feels more like task programming but is down at that kernel authoring layer. Because you've got regular pieces of regular structured data, the compiler understands how it needs to traverse this data and how it needs to do the mapping by communicating enough extra information that this is a dense block of data and here are the dimensions of it.

**38:42** · This is from our very brand new, not yet well-optimized compiler, and it's coming within 10% of a cuDNN program that's been tuned by ninjas for 10 years. cuDNN is literally the state-of-the-art. For us, it's like, "How close are we to cuDNN?" It's always our question. If you're doing something like an inference network, like this, which is a LLaMA 8B inference—it's not huge, but the point is that you can take something like this with all the hard decisions being made by the compiler, and the compiler can understand enough about what you are doing to get within 10% of the state-of-the-art.

**39:17** · I hope that as we work on this compiler over the next few years, we'll add more optimizations and more intelligence and asymptotically approach what that is going to be.

**39:30** · Not everything is data parallel, and not everything is a nice regular bulk array.

**39:35** · So we are not going to take that away from you. You can write tile things in tile arrays, you can do your decompression engines and hashes in thread mode, and pick and choose what you want to do. In the same way, you can add libraries from anywhere you want and put things in frameworks. Don't do any more work than you have to, but every now and then, you're going to have to do some thread kernels, and that's fine. The point is, I'm trying to make that 1% get to 0.1%. If that 1% gets to 0.1%, then I think I'm winning because then I think you are being more productive and getting much better results.

**40:07** · Honestly, the amount of time it would take me to sit down and write a kernel, after 15 years of CUDA experience or more, and write a kernel that would compete with cuDNN within 10% would take me months. This took us a couple of weeks, and it's only the beginning.

**40:24** · So, really, the story of all of these things is to have your cake and eat it too. It's all of the above. We've managed to build enough stuff that implicit parallelism above the line, so that most of your code you never ever have to write a single line of CUDA. I hope we can continue to do that, and you can write less and less CUDA. As one of the architects of CUDA, I hope that I can help you write less CUDA. Every now and then, you have to, but we've got a whole bunch of libraries to help you with it.

**40:56** · When you have to get down and dirty and the libraries don't cover it, we've now got something else on top of that which simplifies that really difficult parallelism that you should avoid at all costs. The more I can make that light green thinner and thinner and thinner, the more you're going to be able to get more stuff done with the GPU, create more interesting algorithms, and we're just going to keep on building more and more pieces on top of that light green so that the secret sauce is kept to an absolute minimum.

**41:25** · Then we're more productive, we get the performance we want, we're more effective, and we've shifted that curve to the left, which I showed you in my imaginary intern curve. So, I think I've probably way overstepped my time, only by 5 minutes, but thank you all very much for listening.