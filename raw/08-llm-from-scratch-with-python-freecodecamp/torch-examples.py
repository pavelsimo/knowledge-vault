# %% [markdown]
# # Torch Examples

# %% Imports & Config
import os
import torch
import time
import torch.nn as nn
import torch.nn.functional as F

# https://www.desmos.com/calculator

def _get_device():
    if torch.cuda.is_available():
        try:
            probe = torch.ones(2, 2).cuda()
            _ = probe @ probe
            return 'cuda'
        except RuntimeError:
            pass
    return 'cpu'

device = _get_device()
print(f"Using device: {device}")

start_time = time.time()

# torch.randint: creates a tensor of random integers in [-100, 100), shape (6,)
random_ints = torch.randint(-100, 100, (6,))
print(random_ints)

# %%
# torch.tensor: constructs a tensor directly from a Python nested list
matrix = torch.tensor([[1, 2, 3], [4, 5, 6]])
print(matrix)

# torch.zeros: creates a tensor filled with 0.0, shape (2, 3)
zeros = torch.zeros(2, 3)
print(zeros)

# torch.ones: creates a tensor filled with 1.0, shape (3, 4)
ones = torch.ones(3, 4)
print(ones)

# torch.empty: allocates an uninitialized tensor, shape (2, 3); values are arbitrary memory
uninitialized = torch.empty(2, 3)
print(uninitialized)

# torch.arange: creates a 1-D tensor with values [0, 1, 2, 3, 4] (like Python range)
sequence = torch.arange(5)
print(sequence)

# torch.linspace: creates 5 evenly spaced values between 3 and 10 (inclusive)
linear_space = torch.linspace(3, 10, steps=5)
print(linear_space)

# torch.logspace: creates 5 values evenly spaced on a log10 scale from 10^-10 to 10^10
log_space = torch.logspace(start=-10, end=10, steps=5)
print(log_space)

# torch.eye: creates a 3x3 identity matrix (1s on diagonal, 0s elsewhere)
identity = torch.eye(3)
print(identity)

# torch.empty_like: allocates an uninitialized tensor with the same shape and dtype as 'matrix'
uninitialized_like = torch.empty_like(matrix)
print(uninitialized_like)

# torch.rand: creates a tensor of random floats in [0.0, 1.0), shape (2, 3)
gpu_mat_a = torch.rand(1000, 1000).to(device)
gpu_mat_b = torch.rand(1000, 1000).to(device)
cpu_mat_a = torch.rand(1000, 1000)
cpu_mat_b = torch.rand(1000, 1000)

# @ operator performs matrix multiplication; result is a (1000, 1000) tensor
matmul_result = gpu_mat_a @ gpu_mat_b

# 10% chance to get a 0, 90% chance to get a 1
probs = torch.tensor([0.1, 0.9])
# torch.multinomial: samples 10 indices from 'probs' with replacement; higher prob means more likely to be sampled
samples = torch.multinomial(probs, num_samples=10, replacement=True)
print("samples:", samples)

# torch.cat: concatenates tensors along a dimension; appends [5] to [1,2,3,4] → [1,2,3,4,5]
base_seq = torch.tensor([1, 2, 3, 4])
extended_seq = torch.cat((base_seq, torch.tensor([5])), dim=0)
print(extended_seq)

# torch.tril: returns the lower-triangular part of a matrix (zeros above the diagonal)
lower_tri = torch.tril(torch.ones(5, 5))
print(lower_tri)

# torch.triu: returns the upper-triangular part of a matrix (zeros below the diagonal)
upper_tri = torch.triu(torch.ones(5, 5))
print(upper_tri)

# step 1 — torch.ones(5,5):      full 5×5 matrix of 1s
# step 2 — torch.tril(...):      zero out above the diagonal → lower-triangular matrix
# step 3 — (... == 0):           boolean mask; True where upper triangle is (positions to block)
# step 4 — torch.zeros((5,5)):   base matrix of 0s (allowed positions will stay 0)
# step 5 — .masked_fill(..., -inf): write -inf at every True position in the mask
# result: 0 where a token can attend (present/past), -inf where it cannot (future)
#         after softmax the -inf positions collapse to 0 probability → causal attention
causal_mask = torch.zeros((5, 5)).masked_fill(torch.tril(torch.ones(5, 5)) == 0, float('-inf'))
print(causal_mask)

attention_weights = torch.exp(causal_mask)
print(attention_weights)

batch_3d = torch.zeros(2, 3, 4)
transposed = batch_3d.transpose(0, 2)
print(transposed.shape)  # should be (4, 3, 2)

row_a = torch.tensor([1, 2, 3])
row_b = torch.tensor([4, 5, 6])
row_c = torch.tensor([7, 8, 9])
stacked = torch.stack([row_a, row_b, row_c], dim=0)
print(stacked)

# torch.nn.Linear: applies a linear transformation to the input data;
# output = input @ weight^T + bias
# https://docs.pytorch.org/docs/2.11/generated/torch.nn.Module.html
input_vector = torch.tensor([10., 10., 10.])  # 1-D input vector of shape (3,)
linear_layer = nn.Linear(3, 3, bias=False)    # weight matrix W of shape (3, 3), no bias term
print(linear_layer(input_vector))             # computes input_vector @ W^T → output shape (3,)

# F.softmax: converts raw scores (logits) into probabilities that sum to 1
# formula: softmax(x_i) = exp(x_i) / sum(exp(x_j) for all j)
logits = torch.tensor([1., 2., 3.])          # raw logits
probs = F.softmax(logits, dim=0)             # dim=0: normalize across the single dimension
print(probs)                                 # tensor([0.0900, 0.2447, 0.6652]) → sums to 1.0


# 3x2 matrix @ 2x3 matrix → 3x3 matrix
a = torch.tensor([[1, 2], [3, 4], [5, 6]])
b = torch.tensor([[7, 8, 9], [10, 11, 12]])
print(a @ b)
print(torch.matmul(a, b))  # equivalent to a @ b


a = torch.tensor([1, 2, 3, 4, 5, 6])
print(a.view(2, 3))  # reshape to 2 rows, 3 columns
print(a.view(3, 2))  # reshape to 3 rows, 2 columns

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")
# %%

