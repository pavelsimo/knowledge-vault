# Neural Networks

Neural networks are computational models composed of stacked layers of simple operations (linear transformations + non-linearities) that learn to approximate complex functions from data. This topic covers the fundamentals: loss functions, regularization, and gradient computation.

## Source

- `raw/03-stanford-cs231n/Stanford CS231N.md`

## From Linear to Non-Linear

A **linear classifier** computes: `f(x; W) = Wx + b`

- `W` is separated by ";" to distinguish model parameters from inputs — standard mathematical notation
- A single layer is just a linear model; it cannot learn non-linear decision boundaries
- **Neural networks = many linear classifiers stacked together** with non-linear activations in between
- More layers = more capacity to learn complex patterns

**Hard cases for linear classifiers:** circular data, XOR patterns, multi-region classes — all require non-linearity.

## Loss Functions

A loss function measures **how bad the model's predictions are**:
- Good predictions → low loss
- Bad predictions → high loss
- Training goal: find weights W that minimize the loss

### Softmax / Cross-Entropy Loss

The **softmax classifier** is standard in modern deep learning:

1. **Raw scores** (logits): `[cat: 3.2, car: 5.1, frog: -1.7]`
2. **Exponentiate** (make positive): `[24.5, 164.0, 0.18]`
3. **Normalize** (sum to 1): `[0.13, 0.87, 0.00]` ← these are probabilities
4. **Loss** = `-log(probability of correct class)` = `-log(0.13) ≈ 2.04`

**Why `-log`?**
- `-log(0.99) ≈ 0.01` → tiny penalty (model was almost right)
- `-log(0.01) = 4.60` → huge penalty (model was very wrong)
- Perfect numerical penalty for how wrong the model is

**Cross-entropy formula:**
```
H(P, Q) = -Σ P(i) log Q(i)
```
Where P = true distribution (one-hot), Q = predicted probabilities.

### Multiclass SVM Loss

```
L = Σ max(0, sⱼ - sᵧ + 1)   for all j ≠ y
```
- Penalizes incorrect class scores that are too close to (or higher than) the correct score
- **Rarely used today** — softmax + cross-entropy has replaced it in all modern frameworks

## Regularization

Regularization prevents overfitting by penalizing model complexity:

```
loss_total = data_loss + λ · regularization_penalty
```

- `λ` (lambda) controls the strength: large λ = strong regularization
- Goal: prefer simpler models that generalize, not complex models that memorize training data

### Types of Regularization

| Type | Penalty |
|------|---------|
| **L2 (Ridge)** | λ · Σ wᵢ² — prefers spread-out, small weights |
| **L1 (Lasso)** | λ · Σ |wᵢ| — promotes sparsity (some weights → 0) |
| **Elastic Net** | Combination of L1 and L2 |
| **Dropout** | Randomly zero out neurons during training |
| **Batch Normalization** | Normalizes activations (implicit regularization) |

**L2 prefers:** weight vector `w2 = [0.25, 0.25, 0.25, 0.25]` over `w1 = [1, 0, 0, 0]` — spreads importance across all features.

## Computing Gradients

Training requires computing the gradient of the loss with respect to all weights.

### Numerical Gradient (Never Use for Training)

```
∂L/∂wᵢ ≈ [L(w + h·eᵢ) - L(w)] / h
```

Problems:
1. **Extremely slow:** O(number of weights) — 10M weights = 10M forward passes
2. **Inaccurate:** floating-point errors when h is small
3. **Sensitive to h:** too large = inaccurate; too small = floating-point dominates
4. **Must repeat for every weight:** impractical for real training

Numerical gradients are only used to **verify** backpropagation implementations (gradient checking).

### Analytic Gradient (Always Use)

**Backpropagation** computes all gradients with one forward pass + one backward pass:
- O(1) relative to model size (constant number of passes regardless of parameter count)
- Exact (not approximated)
- Used in all modern deep learning frameworks

A vector of derivatives = a **gradient**.

## Convex vs Non-Convex Optimization

- **Convex function:** bowl-shaped, single global minimum (e.g., f(x) = x²)
- **Non-convex function:** landscape with many local minima (e.g., f(x) = sin(x))
- **Non-differentiable:** sharp corners where no unique tangent exists (e.g., f(x) = |x|)
- Neural network loss landscapes are **non-convex** — gradient descent finds local minima, not guaranteed global minima

## Related Topics

- [[optimization]] — how gradient descent and its variants minimize the loss
- [[convolutional-neural-networks]] — CNNs built from these fundamentals
- [[recurrent-neural-networks]] — sequential extensions of neural networks
- [[attention-transformers]] — modern architectures using attention mechanisms
- [[probability-statistics]] — the probabilistic interpretation of cross-entropy loss
