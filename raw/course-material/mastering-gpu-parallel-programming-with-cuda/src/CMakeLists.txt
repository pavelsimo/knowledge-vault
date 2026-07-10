# Require CMake version 3.24 or newer.
cmake_minimum_required(VERSION 3.24)

# Create a project named "cuda_hello_world" and enable the CUDA language.
# This tells CMake to find the CUDA Toolkit and use NVCC to compile .cu files.
project(mastering_gpu_parallel_programming_with_cuda LANGUAGES CUDA)

# If the user did not specify which GPU architectures to target,
# build for the architecture of the local GPU ("native").
if(NOT DEFINED CMAKE_CUDA_ARCHITECTURES)
  set(CMAKE_CUDA_ARCHITECTURES native CACHE STRING
      "CUDA architectures to build for")
endif()

add_subdirectory(section_03)
add_subdirectory(section_04)