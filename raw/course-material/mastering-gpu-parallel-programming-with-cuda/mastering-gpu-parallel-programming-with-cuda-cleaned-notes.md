# Mastering GPU Parallel Programming with CUDA - Cleaned Image Notes

Source: `raw/course-material/mastering-gpu-parallel-programming-with-cuda/Mastering GPU Parallel Programming with CUDA.md`

Code: https://github.com/hamdysoltan/CUDA_Course

CUDA Programming: https://docs.nvidia.com/cuda/cuda-programming-guide/index.html#simt-architecture

These are concise study notes rewritten from the raw image-heavy capture. The raw file is preserved as source material.

## CPU vs. GPU

A CPU is optimized for low-latency serial work and complex control flow. A GPU is optimized for high-throughput parallel work, where many simple operations run over many data elements at once.

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/abfd56738e38535d98e832853e28b329_MD5.jpg]]

## GPU Hardware Overview

A GPU is built from repeated compute blocks. At a high level, work is distributed across streaming multiprocessors (SMs), and each SM runs many lightweight threads using local registers, shared memory, schedulers, and execution units.

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/7a42e37ef49401aa1ddfbf8af601bf57_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/377a89600b011de86fa6a82b5f255da7_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/fb79592f4d670a2cdd0689a72ece48a7_MD5.jpg]]

The main mental model: applications launch grids of thread blocks; blocks are assigned to SMs; each SM executes the block's threads in warps.

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/5d3c9861f28c995f51c3500280c51eb0_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/9fc4dabd107e6ab13bdef7d147698715_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/d8dac56860819d23cdaf30afda950e46_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/bdc7254828da8847d1fcb94f176fb11f_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/71d5d65d976602aaf3932c7d59d5d6bc_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/c95ad8e9806907dcb9cafca93b278aad_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/dfa7f79ddda7cb43d554dcd326aa0b21_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/361f668e830c8d1848ac14a830704e8f_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/211b2dc67a3340644d171a21bc3e11b2_MD5.jpg]]

Reference for GPU specs: [TechPowerUp RTX 5090 specs](https://www.techpowerup.com/gpu-specs/geforce-rtx-5090.c4216).

## GPU Model, Chip, Generation, and Architecture

A GPU product name is not the same thing as the chip inside it.

- Generation or series: the product family, such as RTX 50 Series.
- Architecture: the internal design style, such as Blackwell, Ada Lovelace, Ampere, or Turing.
- Chip die: the specific physical silicon used by a card.
- Graphics card design: the board, cooler, power delivery, fans, memory configuration, and factory tuning.

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/61e4b3b597a8149cce30b0631d9ebc1e_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/5196338225563dba034e7704d38102f4_MD5.jpg]]

Example: the [NVIDIA GA100 chip](https://www.techpowerup.com/gpu-specs/nvidia-ga100.g931) is a chip die used in data-center Ampere products.

Different products in the same generation can share an architecture while using different chip dies, memory setups, power limits, and cooling designs. A 90-class model is usually the flagship; 80, 70, and 60-class models are lower tiers with different cost, yield, power, and market targets.

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/d0092b176601f9c37d66886d97dd6e69_MD5.jpg]]

## Same Chip, Different Speeds

Two cards can use similar silicon but perform differently because of enabled core count, clock speed, memory bandwidth, power limits, cooling, and firmware settings.

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/919dd4063d85e4fe966f8d730d8cb4da_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/4cd90a5da9089a80cd45996d21c5af74_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/88b6b6da1acf260a97700d3465429200_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/711a692558b935d0b9984acefd66944f_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/98b7116fd1fd0982795d20e86f8d3021_MD5.jpg]]

## Main GPU Performance Parameters

GPU performance depends on several interacting limits:

- Core count: how many operations can be in flight.
- Clock speed: how many cycles each core can execute per second.
- Memory bandwidth: how quickly data can move to and from VRAM.
- Cache and memory hierarchy: how often data can be reused close to the cores.
- Precision and instruction type: different operations have different throughput.
- Architecture features: Tensor Cores, RT Cores, schedulers, caches, and ISA support.

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/f3de3a667390982f83f9cc9edd92e105_MD5.jpg]]

## Memory Bandwidth

Memory bandwidth measures data movement rate, usually in GB/s. A narrow bus moves less data per cycle; a wider bus and faster memory move more data in the same time.

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/61d91ec276b04b2a2b599e8d9ffc265e_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/d72b6c85fdc019a1008aa347958b7a70_MD5.jpg]]

High memory bandwidth helps workloads that repeatedly stream data, such as games, rendering, video, and large matrix operations. It can improve frame rates and reduce stalls, but only if the workload is bandwidth-limited.

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/18881780e2a97b76f1b1019b6c33ef79_MD5.jpg]]

Bandwidth is mainly determined by bus width, memory speed, and memory technology.

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/f43cddedaeb016008a4531a040572e19_MD5.jpg]]

## Cores, Clocks, Power, and New Hardware Features

More cores do not automatically mean a faster GPU. Clock speed, memory bandwidth, instruction throughput, and workload shape all matter. Higher clocks let each core complete work sooner, but more cores plus higher clocks usually increase power draw and heat.

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/a9474dd029276a7843dbd491cf785c1c_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/ffa045b892dc3a3ce30e38cbfe78d125_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/af72a734c74da502669b0c0de659092d_MD5.jpg]]

Architecture changes can also improve performance without only increasing core count. For example, Tensor Cores introduced in Volta greatly accelerated matrix math compared with Pascal-era CUDA cores alone.

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/9cb4065a62982ad86d7e6c4b53b3e5c5_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/257e9fa1421dcb53c81c0446abc988a5_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/a21f82d2d9db6ecd548826ef60ce2477_MD5.jpg]]

## Precision and Instruction Cost

Operation cost depends on precision and instruction type. FP32, FP16, BF16, INT8, Tensor Core matrix operations, memory instructions, and control-flow instructions can all have different latency and throughput.

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/d96c58791ec87ab2de33084edc57c478_MD5.jpg]]

## Compute Capability

Compute capability is NVIDIA's hardware feature version for CUDA GPUs. It is not a direct speed score. It tells you which CUDA features, PTX instructions, memory operations, and target architectures are supported.

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/9cd34f2de4bca60b6aa0847e2adef0db_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/cf9b34d71aab6da3ea44375f645dcf3a_MD5.jpg]]

Reference: [NVIDIA CUDA compute capability tables](https://docs.nvidia.com/cuda/cuda-programming-guide/05-appendices/compute-capabilities.html).

Compute capability affects which architecture flags you use during compilation, such as `compute_80`, `sm_80`, `compute_89`, or `sm_89`. It also affects compatibility with CUDA toolkit versions and compiled binaries.

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/4cb49734a2cf49e30557b5bcb26cbc0b_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/e41c0d7691d6a7ab8f436000b3d40b67_MD5.jpg]]

## GPU White Papers

To study an NVIDIA chip in detail, search for the architecture or chip name plus "white paper." A typical white paper covers new features, hardware changes, software support, performance graphs, and technical specifications such as cores, memory, bandwidth, and power.

Example: [NVIDIA RTX Blackwell GPU Architecture white paper](https://images.nvidia.com/aem-dam/Solutions/geforce/blackwell/nvidia-rtx-blackwell-gpu-architecture.pdf).

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/cafeee20f40281c83566520efc31ec08_MD5.jpg]]

Pascal-to-Volta changes reduced instruction latency for many GPU operations and added major architectural features.

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/e87c41e6ab01ef228ecf6faf835de989_MD5.jpg]]

Related paper: [Dissecting the NVIDIA Volta GPU Architecture via Microbenchmarking](https://arxiv.org/pdf/1804.06826).

## NVLink and PCIe

PCIe is the standard motherboard interconnect for GPUs, SSDs, NICs, and other devices. NVLink is NVIDIA's high-bandwidth interconnect for faster GPU-to-GPU communication in supported systems.

Use PCIe as the baseline device connection. Use NVLink when multi-GPU workloads need much faster direct GPU communication than PCIe can provide.

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/bd1def91b48b8b3e5300de33cc7fb6b4_MD5.jpg]]

## Warps and Warp Scheduling

A warp is a group of 32 CUDA threads that execute the same instruction together on NVIDIA hardware. CUDA code is written in terms of threads and blocks, but the SM schedules and executes warps.

Example:

```cuda
__global__ void add(int *a, int *b, int *c) {
    int i = threadIdx.x;
    c[i] = a[i] + b[i];
}

add<<<1, 128>>>(a, b, c);
```

The launch creates 128 threads, which the GPU groups into four warps:

```text
warp 0: threads 0-31
warp 1: threads 32-63
warp 2: threads 64-95
warp 3: threads 96-127
```

This execution model is SIMT: single instruction, multiple threads. Unlike classic SIMD, each thread has its own registers and program state, but the warp issues one instruction across 32 lanes.

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/ffe2ea86390a56eb1862b8fe2db9e81c_MD5.jpg]]

The warp scheduler chooses which ready warp should issue next. This helps hide latency: while one warp waits on memory, another warp can run.

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/7647e4f36348222486ce96f445e93111_MD5.jpg]]

## CUDA Toolkit

The CUDA Toolkit contains the compiler driver, runtime, libraries, headers, profiling tools, debugging tools, and documentation needed to build GPU programs.

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/72a8743d3bbe3d5c7bc5a4a0b3c88fde_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/132f6167644db241053fc80b0ee815e2_MD5.jpg]]

Reference: [CUDA Toolkit release notes](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html#).

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/72ee90c244e4c034357330b07522bef7_MD5.jpg]]

## NVCC

NVCC stands for NVIDIA CUDA Compiler Driver. It is a driver, not a single compiler. It separates host code from device code, sends host code to a C++ compiler such as GCC, Clang, or MSVC, sends device code through NVIDIA's CUDA compilation pipeline, and links the result.

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/0719be15f422de16ece9a80466730830_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/89227155d7fc86093540abc2408abb7a_MD5.jpg]]

## CUDA Libraries

CUDA includes specialized libraries so common GPU workloads do not need to be written from scratch. Important examples:

- cuBLAS: dense linear algebra.
- cuFFT: fast Fourier transforms.
- cuRAND: random number generation.
- cuDNN: neural network primitives.

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/a97a529490b3bd2e8b0f7f15ccf70da8_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/ddc4d6cba628a688796b412d2927f67e_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/8e5d7c4e0c6a9874967f3bfe42ddfef6_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/3aa3c0efbae06afa64c1405d8da92b2a_MD5.jpg]]

## Why CUDA is the way it is?

[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/6f877f30692e7427858cf9540ece9f43_MD5.jpg|Open: Pasted image 20260706151540.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/6f877f30692e7427858cf9540ece9f43_MD5.jpg]]

## Is FLOPS the limiting factor for CUDA programs? 

not really, is usually memory bandwidth 

[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/1d302c037a57a37bed79011c08d4d680_MD5.jpg|Open: Pasted image 20260706152619.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/1d302c037a57a37bed79011c08d4d680_MD5.jpg]]

## Host and Device

In CUDA, host means CPU-side code and memory. Device means GPU-side code and memory. CUDA programs usually allocate device memory, copy data from host to device, launch kernels on the device, then copy results back to the host.

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/4565142228ae436f95457fe60113d848_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/2936f4085223d5367b4d1e96011a8066_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/e8b3d26bcad3806637d85d164fc25609_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/755b9eb42881e9ea3e1b73dee7b41f07_MD5.jpg]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/70f1563778c161e44053de4beae89960_MD5.jpg]]

## GigaThread Engine and Block Scheduling

The GigaThread Engine is NVIDIA's global hardware scheduler. It takes thread blocks from a launched grid and assigns them to available SMs.

Its main jobs are:

- Block-to-SM scheduling: assign blocks to SMs with enough registers, shared memory, and warp slots.
- Load balancing: keep SMs busy as blocks finish.
- Context management: switch between work from different kernels or contexts when the hardware supports it.

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/2ecdc62e3d5326ae2fd95b66701682b2_MD5.jpg]]

Blocks are divided into warps because the warp, not the block, is the hardware execution unit. A block is the programmer's logical grouping; the SM executes its threads as groups of 32.

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/7fd0b0e8dd3b2df4677fccba2819c50f_MD5.jpg]]

## PTX

PTX stands for Parallel Thread Execution. It is NVIDIA's virtual GPU instruction set. CUDA source is compiled into PTX or directly into SASS machine code, depending on the build target. PTX can be JIT-compiled for a compatible GPU architecture at runtime.

## Kernel

A Kernel is a function that is executed in the GPU

the `__global__` indicates the function is a kernel

```
// kernel name <<<number of blocks, number of threads per block>>>();
hello_from_gpu <<<1, 1>>>();
```

## Why can't we write 2048?

For example:

```
hello_from_gpu<<<1, 2048>>>();   // ❌ Invalid
```

Because **CUDA defines a maximum block size of 1024 threads** on modern NVIDIA GPUs, including **GB202 (Blackwell)**.

This is a hardware and programming model limit.

- ✅ A **single CUDA block** can contain **at most 1024 threads** on GB202 and other modern NVIDIA GPUs.
- ✅ Those 1024 threads are split into **32 warps of 32 threads each**.
- ✅ The GPU can execute **millions of threads** overall by launching **many blocks**.
- ❌ The 1024 limit applies **per block**, not to the entire GPU.

1024 threads
│
├── Warp 0   (threads 0-31)
├── Warp 1   (32-63)
├── Warp 2   (64-95)
...
└── Warp 31  (992-1023)

Total = 32 warps

## What is cudaDeviceSynchronize();?

This tells the CPU to wait on the GPU threads:

```
hello_from_gpu <<<2, 64>>>();
cudaDeviceSynchronize();
```



[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/86daafd6ce397fe8db65d712de002e2a_MD5.jpg|Open: Pasted image 20260628112309.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/86daafd6ce397fe8db65d712de002e2a_MD5.jpg]]

## Vector Addition

CPU:

[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/809174c305808637d02d1cfd6ad2b004_MD5.jpg|Open: Pasted image 20260628114214.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/809174c305808637d02d1cfd6ad2b004_MD5.jpg]]

GPU:

[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/7a3da0557c02d2c190eb9019186bab9c_MD5.jpg|Open: Pasted image 20260628114521.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/7a3da0557c02d2c190eb9019186bab9c_MD5.jpg]]

### Steps

[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/7f1cf52263e1f0d7d217b86c091bbcf3_MD5.jpg|Open: Pasted image 20260628114813.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/7f1cf52263e1f0d7d217b86c091bbcf3_MD5.jpg]]

[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/84790fc4d027fb5171a20f3925d706da_MD5.jpg|Open: Pasted image 20260628114900.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/84790fc4d027fb5171a20f3925d706da_MD5.jpg]]

[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/87344da38690e706504c96945c6e2ba6_MD5.jpg|Open: Pasted image 20260628115148.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/87344da38690e706504c96945c6e2ba6_MD5.jpg]]

[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/d8db71843e5fa58b4d756d692681205e_MD5.jpg|Open: Pasted image 20260628115237.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/d8db71843e5fa58b4d756d692681205e_MD5.jpg]]

[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/6e2429336a3705f26c9cdde3b449d8fb_MD5.jpg|Open: Pasted image 20260628115331.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/6e2429336a3705f26c9cdde3b449d8fb_MD5.jpg]]

[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/fda2397184bdd23460239bf79d98f47d_MD5.jpg|Open: Pasted image 20260628115529.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/fda2397184bdd23460239bf79d98f47d_MD5.jpg]]

[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/10f6bb8e66d09b5be27852d21dcd5787_MD5.jpg|Open: Pasted image 20260628115554.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/10f6bb8e66d09b5be27852d21dcd5787_MD5.jpg]]

adding arrays with more than 1024 elements 

[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/d44f89d3700add2b18bf4af99bab63f4_MD5.jpg
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/d44f89d3700add2b18bf4af99bab63f4_MD5.jpg]]   


[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/afdd2a0f2fd99ed6d02dd58a11915d8f_MD5.jpg|Open: Pasted image 20260628152712.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/afdd2a0f2fd99ed6d02dd58a11915d8f_MD5.jpg]]

GPU (the whole company)
│
├── SM (departments)
│   ├── Block
│   │   ├── Warp
│   │   │   ├── Thread
│   │   │   ├── Thread
│   │   │   └── ...
│   │   └── Warp
│   └── Block
└── ...

[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/fbccf887c9d3ac497a2e1cf993f69544_MD5.jpg|Open: Pasted image 20260628153239.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/fbccf887c9d3ac497a2e1cf993f69544_MD5.jpg]]


## What is the Runtime API?

https://docs.nvidia.com/cuda/cuda-runtime-api/index.html


[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/8bc9d20c21648cb4d2aa86dea63b862a_MD5.jpg|Open: Pasted image 20260628165033.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/8bc9d20c21648cb4d2aa86dea63b862a_MD5.jpg]]

### Important Runtime information

| Field                                           | Meaning                                                                                                                                                                                                                                                                                                                                                                                       |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Device 0: NVIDIA GeForce RTX 5090**           | CUDA numbers visible GPUs starting at 0. “Device 0” is the first CUDA-visible GPU in the system. It does not necessarily mean the first physical PCIe slot.                                                                                                                                                                                                                                   |
| **Compute capability: 12.0**                    | The CUDA architecture version supported by the GPU. It determines which CUDA features, instructions, tensor-core behavior, memory features, and compiler targets are available. For compiling CUDA code, this corresponds conceptually to targeting something like `sm_120`.                                                                                                                  |
| **Total global memory: 31.36 GB**               | The amount of GPU VRAM available for CUDA allocations. “Global memory” is the large off-chip memory used for tensors, arrays, model weights, activations, textures, etc. It is much larger than shared memory but also much slower.                                                                                                                                                           |
| **Shared memory per block: 49152 bytes**        | The maximum shared memory available to one CUDA thread block, here **49,152 bytes**, or **48 KiB**. Shared memory is fast on-chip memory shared by threads in the same block. It is often used for tiling matrix multiplication, stencil operations, reductions, histograms, and avoiding repeated global-memory reads.                                                                       |
| **Registers per block: 65536**                  | The maximum number of registers one thread block can use, here **65,536 32-bit registers**. Registers are the fastest per-thread storage. If each thread uses many registers, fewer threads or blocks may fit on an SM, reducing occupancy. For example, a block with 1,024 threads can use at most 64 registers per thread before hitting this block-level limit.                            |
| **Warp size: 32**                               | CUDA threads execute in groups called **warps**. One warp contains **32 threads**. This is why CUDA block sizes are commonly multiples of 32, such as 128, 256, 512, or 1024 threads. Branch divergence matters at the warp level: if threads in the same warp take different branches, execution may serialize.                                                                              |
| **Max threads per block: 1024**                 | A single CUDA block may contain at most **1,024 threads** total. For example, `dim3 block(1024)`, `dim3 block(32, 32)`, and `dim3 block(16, 16, 4)` are valid shapes because their products are at most 1,024.                                                                                                                                                                                |
| **Max threads per dimension: (1024, 1024, 64)** | These are the maximum sizes for the `x`, `y`, and `z` dimensions of a single block. So `blockDim.x <= 1024`, `blockDim.y <= 1024`, and `blockDim.z <= 64`. The product still cannot exceed **1024 threads per block**. For example, `(1024, 1, 1)` is valid, `(32, 32, 1)` is valid, but `(1024, 1024, 1)` is not, because that would be over one million threads in one block.               |
| **Max grid size: (2147483647, 65535, 65535)**   | These are the maximum numbers of blocks in the `x`, `y`, and `z` dimensions of a kernel launch grid. The `x` dimension can be extremely large: **2,147,483,647 blocks**. The `y` and `z` dimensions are limited to **65,535 blocks** each. This controls how many blocks you can launch, not how many threads are in each block.                                                              |
| **Memory clock rate: 14.00 GHz**                | The clock rate associated with the GPU memory. This is used, together with the memory bus width and transfer mode, to estimate peak memory bandwidth. Real applications usually achieve less than the peak because of access patterns, cache behavior, instruction overhead, and memory-controller efficiency.                                                                                |
| **Memory bus width: 512 bits**                  | The width of the memory interface between the GPU and its VRAM. A **512-bit** bus means the GPU can move 512 bits, or **64 bytes**, per memory transfer cycle across the full memory interface. Wider bus = more potential bandwidth, assuming high enough memory clock.                                                                                                                      |
| **Peak memory bandwidth: 1792.13 GB/s**         | The theoretical maximum rate at which the GPU can move data to/from VRAM. Roughly: `14 GHz × 512 bits / 8 × 2 ≈ 1792 GB/s`. The `/8` converts bits to bytes, and the extra factor accounts for double-data-rate-style transfers. This is a theoretical ceiling; actual bandwidth depends heavily on coalescing, access patterns, cache hits, and workload.                                    |
| **L2 cache size: 100663296 bytes (96.00 MB)**   | The size of the GPU’s L2 cache. `100,663,296 bytes` is **96 MiB**. L2 cache sits between the SMs and global memory. It helps when data is reused, when memory accesses are spatially or temporally local, or when multiple SMs access overlapping data. A large L2 can significantly improve performance for bandwidth-sensitive workloads.                                                   |
| **Multiprocessors (SM count): 170**             | The GPU has **170 Streaming Multiprocessors**, or SMs. SMs are the main execution units of an NVIDIA GPU. CUDA blocks are scheduled onto SMs, and each SM runs warps. More SMs generally mean more parallel compute capacity, though actual performance also depends on clocks, instruction mix, memory bandwidth, occupancy, and tensor-core usage.                                          |
| **Concurrent kernels: yes**                     | The GPU can run multiple CUDA kernels at the same time, usually when they are launched in different CUDA streams and when resources allow. This does not guarantee that every pair of kernels will overlap; large kernels that consume all SMs, registers, shared memory, or memory bandwidth may still effectively run alone.                                                                |
| **ECC enabled: no**                             | Error-Correcting Code memory is not enabled. ECC can detect and correct some memory errors, which is useful in servers, scientific computing, finance, and long-running jobs. Consumer GeForce cards typically do not expose ECC in the same way as data-center GPUs. With ECC off, you get full available memory capacity and no ECC overhead, but less protection against memory bit flips. |

[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/59be87cde7998d630ce1b89346af29f5_MD5.jpg|Open: Pasted image 20260628212931.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/59be87cde7998d630ce1b89346af29f5_MD5.jpg]]

## What is nvidia-smi?

SMI stands for system management interface

- Performance monitoring
- Settings management 
- Device information querying 


[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/3a6d32b7d2c8d9fb503a83023f7bb4e7_MD5.jpg|Open: Pasted image 20260628213358.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/3a6d32b7d2c8d9fb503a83023f7bb4e7_MD5.jpg]]
[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/0ee62e9068c9c8bf32bf54e433f3964c_MD5.jpg|Open: Pasted image 20260628214929.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/0ee62e9068c9c8bf32bf54e433f3964c_MD5.jpg]]

```

# monitoring gpu every 5 seconds
> nvidia-smi -l 5

# display specific information
> nvidia-smi --query-gpu=gpu_name,driver_version,temperature.gpu --format=csv
name, driver_version, temperature.gpu
NVIDIA GeForce RTX 5090, 595.71.05, 43

```

[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/a25e8dae5b75caf3c312f517c350eefd_MD5.jpg|Open: Pasted image 20260628215839.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/a25e8dae5b75caf3c312f517c350eefd_MD5.jpg]]

you can either view the current clocks or change the a clock frequency for the GPU:

| Field        | Meaning                                                                                                                                                                                                                                                                                            |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Graphics** | Current graphics/shader clock. This is the main GPU core-style clock exposed for graphics/shader work. NVIDIA labels it as the graphics “shader” clock. ([NVIDIA Docs](https://docs.nvidia.com/deploy/nvidia-smi/index.html "docs.nvidia.com"))                                                    |
| **SM**       | Current Streaming Multiprocessor clock. This is the clock for the SMs, where CUDA cores, Tensor Cores, and much of compute execution live. NVIDIA defines this as the SM / Streaming Multiprocessor clock. ([NVIDIA Docs](https://docs.nvidia.com/deploy/nvidia-smi/index.html "docs.nvidia.com")) |
| **Memory**   | Current VRAM memory clock. Yours is only **405 MHz**, which usually means the memory is in a low-power/idle clock state.                                                                                                                                                                           |
| **Video**    | Current video engine clock, used by the hardware encoder/decoder blocks, commonly NVENC/NVDEC. NVIDIA describes this as the video encoder + decoder clock. ([NVIDIA Docs](https://docs.nvidia.com/deploy/nvidia-smi/index.html "docs.nvidia.com"))                                                 |
## What is Occupancy?

Is a measure of the utilization of the resources in a GPU.

[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/a1697d7d3a1e02bc272aefa09d1b8234_MD5.jpg|Open: Pasted image 20260628222247.png]]

![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/a1697d7d3a1e02bc272aefa09d1b8234_MD5.jpg]]

[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/96a0bd5b106d2b378bb8755045d615e6_MD5.jpg|Open: Pasted image 20260628222400.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/96a0bd5b106d2b378bb8755045d615e6_MD5.jpg]]

### Why the max threads per SM is 1536 and max warps is 48? is not suppose to be 1024?

This is a very common point of confusion when looking at CUDA specifications: mixing up the limits of a **Thread Block** with the limits of a **Streaming Multiprocessor (SM)**.

Here is the breakdown of why those numbers are what they are, and where that 1024 limit actually applies.
### 1. The "1024" Limit is for Blocks, not SMs

You are entirely correct that the number **1024** is a hard limit in modern NVIDIA architectures, but it is the maximum number of threads allowed in a single **Thread Block**, not a single SM.

- **Thread Block Limit:** A single block cannot contain more than 1024 threads.
- **SM Limit:** An SM is the actual physical hardware unit on the GPU. A single SM is designed to execute _multiple_ thread blocks concurrently.

So, if an SM has a maximum capacity of 1536 threads, it cannot run them all as one giant block. Instead, it might run:

- One block of 1024 threads + one block of 512 threads.
- Three blocks of 512 threads.
- Six blocks of 256 threads.

As long as the total number of threads across all active blocks on that specific SM does not exceed 1536, the workload is valid.

### 2. The Math Behind 1536 and 48

In CUDA architecture, threads are grouped into **Warps** for execution.
- **1 Warp = 32 Threads** (This is a universal constant in modern NVIDIA GPUs).
    
The two numbers you provided are directly tied to each other by this rule:
- 48 maximum warps per SM × 32 threads per warp = **1536 maximum threads per SM**.
### Why 1536 specifically?

The maximum number of threads an SM can handle is dictated by the specific microarchitecture of the GPU.

The **1536 threads / 48 warps per SM** limit is the exact hardware specification for both the **Ampere** architecture (which includes cards like the RTX 3090) and the **Ada Lovelace** architecture (which includes the RTX 4000 and RTX 5000 workstation series).

If you were looking at an older Turing architecture card (like an RTX 2080), you _would_ actually see a limit of 1024 threads (32 warps) per SM. Conversely, if you look at the newer Hopper architecture designed for heavy data center workloads, the SMs are beefed up to handle 2048 threads (64 warps) per SM.

When you are writing or tuning CUDA kernels for architectures like Ampere or Ada, knowing that the SM ceiling is 1536 is critical for maximizing occupancy. If you launch blocks of exactly 1024 threads, you will "strand" 512 threads of capacity on the SM, because there isn't enough room to fit a second 1024-thread block.

[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/9886bf035abfe8eca23d77814655fde6_MD5.jpg|Open: Pasted image 20260628233604.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/9886bf035abfe8eca23d77814655fde6_MD5.jpg]]

## What is the cli tool ncu?

NVIDIA Nsight Compute CLI (ncu) provides a non-interactive way to profile applications from the command line. It can print the results directly on the command line or store them in a report file. It can also be used to simply launch the target application (see [General](https://docs.nvidia.com/nsight-compute/NsightComputeCli/index.html#command-line-options-general) for details) and later attach with NVIDIA Nsight Compute or another ncu instance.

https://docs.nvidia.com/nsight-compute/NsightComputeCli/index.html

## How to profile with ncu?

```
ncu ./build/section_03/vector_addition_3
```

## What is theoretical occupancy?


[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/6128ee3ad0350ff21bedbb5052b81104_MD5.jpg|Open: Pasted image 20260705235003.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/6128ee3ad0350ff21bedbb5052b81104_MD5.jpg]]

## What is achieved occupancy?

[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/3b904be31622b50f1151562c680dd6cb_MD5.jpg|Open: Pasted image 20260705235200.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/3b904be31622b50f1151562c680dd6cb_MD5.jpg]]


[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/3e00d0536adadb740fdbfcf40f8a0aa2_MD5.jpg|Open: Pasted image 20260706000625.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/3e00d0536adadb740fdbfcf40f8a0aa2_MD5.jpg]]

[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/63163f19a0ba2f7401fe7de6e9306015_MD5.jpg|Open: Pasted image 20260706234239.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/63163f19a0ba2f7401fe7de6e9306015_MD5.jpg]]

[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/79357b66f761878a280be2eb43f79fa5_MD5.jpg|Open: Pasted image 20260708235937.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/79357b66f761878a280be2eb43f79fa5_MD5.jpg]]

### SASS (Streaming Assembler)

SASS is the low-level assembly language (the Instruction Set Architecture or ISA) specific to NVIDIA GPUs.

- **The "Machine Code":** While PTX (Parallel Thread Execution) acts as an intermediate, hardware-agnostic representation that looks somewhat like C++, SASS is the actual hardware-dependent assembly that the GPU's scheduler and execution units process.
    
- **Architecture Dependent:** Because SASS maps directly to the physical hardware (such as the register files and functional units shown on the right side of **image_643dbd.jpg**), it changes with every GPU architecture generation (e.g., Ampere, Hopper, Blackwell).
    
- **Execution:** It is what the Warp Scheduler actually feeds into the execution pipelines.


### NVBit (NVIDIA Binary Instrumentation Tool)

NVBit is a dynamic binary instrumentation framework specifically designed for NVIDIA GPUs.

- **Instruction Injection:** It allows you to inject custom code into the SASS stream _at runtime_. Rather than modifying the source code or the PTX, NVBit lets you intercept the execution of a kernel to trace instructions, profile memory access, or perform fine-grained performance analysis.
    
- **The "Hook":** In the context of the workflow often depicted in academic or technical GPU presentations, NVBit acts as the bridge between your analysis tools and the physical instruction execution. It is what makes it possible to inspect the "Occupancy and hiding latency" mentioned at the top of **image_643dbd.jpg** by monitoring how individual threads and warps behave in real-time.

### Why use Partitions?

Instead of having one massive, complex scheduler trying to manage hundreds of warps and route them to dozens of execution units across the entire SM, partitioning divides the labor.

By giving each partition its own scheduler, register file, and set of math cores, the GPU can concurrently schedule and execute multiple instructions per clock cycle across the SM with much lower latency and hardware complexity.

[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/bd2add3c064d90bcaad66160314df473_MD5.jpg|Open: Pasted image 20260708235312.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/bd2add3c064d90bcaad66160314df473_MD5.jpg]]

[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/4050da75a669a68a26118976893890ca_MD5.jpg|Open: Pasted image 20260706151301.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/4050da75a669a68a26118976893890ca_MD5.jpg]]

## Important points regarding occupancy

[[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/64d0708649222bf417e3ae13db7a4bba_MD5.jpg|Open: Pasted image 20260708233845.png]]
![[raw/course-material/mastering-gpu-parallel-programming-with-cuda/images/64d0708649222bf417e3ae13db7a4bba_MD5.jpg]]

