#include <cuda_runtime.h>
#include <stdio.h>
#include <cuda.h>

#define NUM_BLOCKS 1024
#define THREADS_PER_BLOCK 256
#define SIZE (1 << 24)   // 16M elements
#define CHUNK_SIZE (NUM_BLOCKS * THREADS_PER_BLOCK)

__global__ void add_vec(int *a, int *b, int *c)
{
	int i = blockIdx.x * blockDim.x + threadIdx.x;
	c[i] = a[i] + b[i];
}

int main(void)
{
	int *ha, *hb, *hc;
	int *da, *db, *dc;
	int chunk_sz = CHUNK_SIZE * sizeof(int);
	int total_sz = SIZE * sizeof(int);

	/* Step 1: Allocate host memory — inputs chunk-sized, output full-sized */
	ha = (int *)malloc(chunk_sz);
	hb = (int *)malloc(chunk_sz);
	hc = (int *)malloc(total_sz);

	/* Step 2: Allocate device memory for one chunk only */
	cudaMalloc((void **)&da, chunk_sz);
	cudaMalloc((void **)&db, chunk_sz);
	cudaMalloc((void **)&dc, chunk_sz);

	cudaEvent_t start, stop;
	cudaEventCreate(&start);
	cudaEventCreate(&stop);

	cudaEventRecord(start);

	/* Step 3: Process each chunk — SIZE must be a multiple of CHUNK_SIZE */
	for (int offset = 0; offset < SIZE; offset += CHUNK_SIZE) {
		for (int i = 0; i < CHUNK_SIZE; i++) {
			ha[i] = offset + i + 1;
			hb[i] = offset + i + 1;
		}

		cudaMemcpy(da, ha, chunk_sz, cudaMemcpyHostToDevice);
		cudaMemcpy(db, hb, chunk_sz, cudaMemcpyHostToDevice);

		add_vec<<<NUM_BLOCKS, THREADS_PER_BLOCK>>>(da, db, dc);

		cudaMemcpy(hc + offset, dc, chunk_sz, cudaMemcpyDeviceToHost);
	}

	cudaEventRecord(stop);
	cudaEventSynchronize(stop);

	float milliseconds = 0;
	cudaEventElapsedTime(&milliseconds, start, stop);
	printf("Time elapsed: %f ms\n", milliseconds);

	cudaFree(da);
	cudaFree(db);
	cudaFree(dc);
	free(ha);
	free(hb);
	free(hc);

	cudaDeviceSynchronize();
	return 0;
}
