#include <cuda_runtime.h>
#include <stdio.h>

#define MAX_THREADS_PER_BLOCK 1024
#define SIZE 2048

__global__ void add_vec(int *a, int *b, int *c, int n)
{
	// blockIdx.x  = block index in the grid
	// blockDim.x  = number of threads per block
	// threadIdx.x = thread index within the block
	int i = blockIdx.x * blockDim.x + threadIdx.x;
	c[i] = a[i] + b[i];
}

int main(void)
{
	int *ha, *hb, *hc;
	int *da, *db, *dc;
	int sz = SIZE * sizeof(int);

	/* Step 1: Allocate host memory */
	ha = (int *)malloc(sz);
	hb = (int *)malloc(sz);
	hc = (int *)malloc(sz);

	/* Step 2: Allocate device memory */
	cudaMalloc((void **)&da, sz);
	cudaMalloc((void **)&db, sz);
	cudaMalloc((void **)&dc, sz);

	/* Step 3: Initialize host arrays */
	for (int i = 0; i < SIZE; i++) {
		ha[i] = i + 1;
		hb[i] = i + 1;
	}

	/* Step 4: Copy host arrays to device */
	cudaMemcpy(da, ha, sz, cudaMemcpyHostToDevice);
	cudaMemcpy(db, hb, sz, cudaMemcpyHostToDevice);

	/* Step 5: Launch kernel */
	add_vec<<<SIZE / MAX_THREADS_PER_BLOCK, MAX_THREADS_PER_BLOCK>>>(da, db, dc, SIZE);

	/* Step 6: Copy result back to host */
	cudaMemcpy(hc, dc, sz, cudaMemcpyDeviceToHost);

	/* Step 7: Print result */
	printf("The result of vector addition is:\n");
	for (int i = 0; i < SIZE; i++) {
		printf("%d + %d = %d\n", ha[i], hb[i], hc[i]);
	}

	cudaFree(da);
	cudaFree(db);
	cudaFree(dc);
	free(ha);
	free(hb);
	free(hc);

	cudaDeviceSynchronize();
	return 0;
}
