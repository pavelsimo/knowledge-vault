# CUDA Hello World

Minimal C-style CUDA starter for the Mastering GPU Parallel Programming with CUDA course material.

## Build

This example uses CMake and NVIDIA's CUDA compiler (`nvcc`).

```sh
cmake -S . -B build
cmake --build build
```

To target a specific GPU architecture instead of CMake's native detection, pass `CMAKE_CUDA_ARCHITECTURES` explicitly. For example, an RTX 5090 reports compute capability 12.0:

```sh
cmake -S . -B build -DCMAKE_CUDA_ARCHITECTURES=120
cmake --build build
```

## Run

```sh
./build/cuda_hello
```

Expected output:

```text
Hello World from CPU.
Hello World from GPU block 0, thread 0.
Hello World from GPU block 0, thread 1.
Hello World from GPU block 0, thread 2.
Hello World from GPU block 0, thread 3.
```

The GPU lines may appear in a different order because CUDA threads execute in parallel.
