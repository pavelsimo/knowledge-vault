---
title: "Warp Scheduling (GPU Thread Scheduling)"
source: "https://stevengong.co/notes/Warp-Scheduling"
author:
published:
created: 2026-07-06
description: "Streaming Multiprocessor Warp Scheduling (GPU Thread Scheduling) How do instructions get scheduled on the GPU? This article is a really good overview."
tags:
  - "clippings"
---
[Streaming Multiprocessor](https://stevengong.co/notes/Streaming-Multiprocessor)

[

## Streaming Multiprocessor (SM)

](https://stevengong.co/notes/Streaming-Multiprocessor)

[A Streaming Multiprocessor (SM) is a fundamental component of NVIDIA GPUs, consisting of multiple](https://stevengong.co/notes/Streaming-Multiprocessor) [Stream Processor](https://stevengong.co/notes/CUDA-Core) s (CUDA Core) responsible for executing instructions in parallel.

They are general purpose processors with a low clock rate target and a small cache.

![[raw/clippings/images/eedb464925d77de93bb83dd70822bd25_MD5.png]]

- Inside a GA100 SM, source: [Ampere whitepaper](https://images.nvidia.com/aem-dam/en-zz/Solutions/data-center/nvidia-ampere-architecture-whitepaper.pdf)

Consists of:

- SUPER LARGE [Register File](https://stevengong.co/notes/Register-File)
	- This is how they can context switch quickly with no overhead, by keeping data on registers, see [Warp Scheduling](https://stevengong.co/notes/Warp-Scheduling)
- Caches and shared memory
- [Warp Scheduler](https://stevengong.co/notes/Warp-Scheduling)
- Execution units ([SFU](https://stevengong.co/notes/Special-Function-Unit) s, [CUDA Core](https://stevengong.co/notes/CUDA-Core) s and [Tensor Core](https://stevengong.co/notes/Tensor-Core) s)

> Task of SM
> 
> SMs execute several thread blocks in parallel. As soon as one of its thread block has completed execution, it takes up the serially next thread block.

From [Stephen Jones](https://stevengong.co/notes/Stephen-Jones), I learned that each SM can managed 64 warps, so a total of 2048 threads. However, it really processes 4 warps at a time (see [Warp Scheduling](https://stevengong.co/notes/Warp-Scheduling)).

![[raw/clippings/images/d92356eeee1c5c47f4235ae18c48b82d_MD5.png]]

- Source: [How CUDA Programming Works | GTC 2022](https://www.youtube.com/watch?v=n6M8R8-PlnE&ab_channel=PERLI)

![[raw/clippings/images/02c6a411a00036904c591cb5c00e6f7e_MD5.png]]

Resources

- [Stephen Jones](https://stevengong.co/notes/Stephen-Jones)
- [http://thebeardsage.com/cuda-streaming-multiprocessors/](http://thebeardsage.com/cuda-streaming-multiprocessors/)
- [https://en.wikipedia.org/wiki/Thread\_block\_(CUDA\_programming)](https://en.wikipedia.org/wiki/Thread_block_\(CUDA_programming\))
- [https://saturncloud.io/blog/an-introduction-to-streaming-multiprocessors-blocks-and-threads-in-cuda/](https://saturncloud.io/blog/an-introduction-to-streaming-multiprocessors-blocks-and-threads-in-cuda/)
- [https://stackoverflow.com/questions/3519598/streaming-multiprocessors-blocks-and-threads-cuda](https://stackoverflow.com/questions/3519598/streaming-multiprocessors-blocks-and-threads-cuda) (clarifies CUDA core and CUDA warp)

> How many thread blocks at the same time?
> 
> An SM may contain up to 8 thread blocks in total.

> Branch prediction?
> 
> In general, SMs support instruction-level parallelism but not branch prediction.

![[raw/clippings/images/c6fea242fb1db17af5cc9910f74db428_MD5.png]]

Each architecture in GPU consists of several SM.

## Warp Scheduling (GPU Thread Scheduling)

How do instructions get scheduled on the GPU? This [article](http://thebeardsage.com/cuda-streaming-multiprocessors/) is a really good overview.

You should actually read NVIDIA docs, the official source of truth:

- [https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#simt-architecture](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#simt-architecture)

When a block is divided up into warps, each warp is assigned to a *warp scheduler*.

- Reminder that a warp is composed of **32 threads** of code (see [CUDA Kernel](https://stevengong.co/notes/CUDA-Examples))

Warps will stay on the *assigned scheduler for the lifetime* of the warp.

VERY IMPORTANT: The scheduler is able to switch between concurrent warps, originating from any block of any kernel, **without overhead**. - [Source](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#hardware-multithreading)

> Why is it possible without overhead?
> 
> Because the data is maintained inside the register file. Unlike a CPU, where when you context switch, you need to store the state of the registers into memory, in your SM, you can just be like “I’ll switch to another warp and come back after”, without modifying the state of the registers.
> 
> “When switching away from a particular warp, all the data of that warp remains in the register file so that it can be quickly resumed when its [Operand](https://stevengong.co/notes/Operand) s become ready”. [wikipedia](https://en.wikipedia.org/wiki/Thread_block_\(CUDA_programming\))

![[raw/clippings/images/cafa3100b279cdb2031fd17b102d2973_MD5.png]]

The [SM](https://stevengong.co/notes/Streaming-Multiprocessor) processes 4 warps at the same time in a given cycle.

> Why 4?
> 
> Because there are 4 warp schedulers per SM.

> but isn't there synchronization needed, seeds the schedulers read the same instruction?
> 
> Each scheduler manages **its own queue of warps**. and selects a warp to issue an instruction to the execution units. Warps are independent execution units (SIMD-style execution).

Essentially, in a given cycle, there are up to 4 warps that can be assigned “work”, if there are 4 warp schedulers.

### What happens at a thread level?

This was the thing that I was always confused about, but reading about the NVIDIA docs helps a bit more.

- [https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#simt-architecture](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#simt-architecture)

A warp executes one common instruction at a time, so **full efficiency** is realized when all 32 threads of a warp agree on their execution path.

Branch divergence occurs only within a warp; different warps execute independently regardless of whether they are executing common or disjoint code paths.

Since NVIDIA Volta, the GPU maintains **execution state per thread**, including a program counter and call stack.

> Each thread has its own program counter!
> 
> This is very important, it allows full **concurrency between threads**.
> 
> “Prior to NVIDIA Volta, warps used a single program counter shared amongst all 32 threads in the warp together with an active mask specifying the active threads of the warp”.

In the next cycle, the warp scheduler can dispatch more instructions to free warps. As computation is being done, some of these warps will become blocked.

- In a CPU, a core could also be blocked. In which case the OS can context switch to another process. But this is slow because we need to save the state of the registers. But for GPU programming, because we have so many warps and thus registers, we can just switch to another free warp to do work.

If more than one warps are eligible for execution, the parent SM uses a warp scheduling policy for deciding which warp gets the next fetched instruction.

![[raw/clippings/images/7a70b94fe3424e3430ee812565dbe554_MD5.png]]

> Why does a warp scheduler have 2 instruction dispatch?
> 
> Is this inspo from how we do CPUs with [Hyperthreading](https://stevengong.co/notes/Simultaneous-Multithreading)? Seems like it.
> 
> At each cycle the scheduler selects a warp, and if possible, two independent instructions will be issued to that warp.
> 
> - They must be mapped to different functional units (e.g., one ALU operation and one memory operation)