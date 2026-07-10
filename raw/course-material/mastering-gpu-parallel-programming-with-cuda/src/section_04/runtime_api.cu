#include <cuda_runtime.h>
#include <stdio.h>

int main(void)
{
	int device_count = 0;
	cudaGetDeviceCount(&device_count);
	printf("Number of CUDA devices: %d\n", device_count);

	for (int dev = 0; dev < device_count; dev++) {
		cudaDeviceProp prop;
		cudaGetDeviceProperties(&prop, dev);

		printf("\nDevice %d: %s\n", dev, prop.name);
		printf("  Compute capability:          %d.%d\n", prop.major, prop.minor);
		printf("  Total global memory:         %.2f GB\n", (double)prop.totalGlobalMem / (1 << 30));
		printf("  Shared memory per block:     %zu bytes\n", prop.sharedMemPerBlock);
		printf("  Registers per block:         %d\n", prop.regsPerBlock);
		printf("  Warp size:                   %d\n", prop.warpSize);
		printf("  Max threads per block:       %d\n", prop.maxThreadsPerBlock);
		printf("  Max threads per dimension:   (%d, %d, %d)\n", prop.maxThreadsDim[0], prop.maxThreadsDim[1], prop.maxThreadsDim[2]);
		printf("  Max grid size:               (%d, %d, %d)\n", prop.maxGridSize[0], prop.maxGridSize[1], prop.maxGridSize[2]);
		int mem_clock_khz = 0;
		cudaDeviceGetAttribute(&mem_clock_khz, cudaDevAttrMemoryClockRate, dev);
		printf("  Memory clock rate:           %.2f GHz\n", mem_clock_khz / 1e6);
		printf("  Memory bus width:            %d bits\n", prop.memoryBusWidth);
		printf("  Peak memory bandwidth:       %.2f GB/s\n", 2.0 * mem_clock_khz * (prop.memoryBusWidth / 8) / 1e6);
		printf("  L2 cache size:               %d bytes (%.2f MB)\n", prop.l2CacheSize, (double)prop.l2CacheSize / (1 << 20));
		printf("  Multiprocessors (SM count):  %d\n", prop.multiProcessorCount);
		printf("  Max threads per SM:          %d\n", prop.maxThreadsPerMultiProcessor);
		printf("  Max warps per SM:            %d\n", prop.maxThreadsPerMultiProcessor / prop.warpSize);
		printf("  Concurrent kernels:          %s\n", prop.concurrentKernels ? "yes" : "no");
		printf("  ECC enabled:                 %s\n", prop.ECCEnabled ? "yes" : "no");
	}

	return 0;
}
