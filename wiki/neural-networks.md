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

**Hard cases for linear classifiers (three canonical failure modes):**
- **XOR/quadrant problem:** Class 1 in quadrants 1 & 3, Class 2 in quadrants 2 & 4. No single line can separate them.
- **Donut problem:** Class 1 in a ring (1 ≤ L2 norm ≤ 2), Class 2 everywhere else. The boundary is circular.
- **Multi-modal class:** Class 1 appears as three separated blobs, Class 2 is everything else. No connected linear region can capture all three.

All three require non-linearity to solve.

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

### Multiclass SVM Loss (Hinge Loss)

```
Lᵢ = Σⱼ≠ᵧᵢ max(0, sⱼ - sᵧᵢ + 1)
```
Where:
- `sⱼ` = score for (incorrect) class j
- `sᵧᵢ` = score for the correct class
- `1` = margin — penalizes any incorrect class whose score is within 1 of the correct score

For every incorrect class: if the incorrect score is higher than (correct score − 1), add that gap as loss. Otherwise add zero. Total loss per example = sum of all penalties.

- **Rarely used today** — softmax + cross-entropy has replaced it in all modern frameworks (PyTorch, TensorFlow, JAX)

### Regularization Formulas

From the slides, the three regularization penalties explicitly:

```
L2: R(W) = Σₖ Σₗ W²ₖ,ₗ
L1: R(W) = Σₖ Σₗ |Wₖ,ₗ|
Elastic net: R(W) = Σₖ Σₗ βW²ₖ,ₗ + |Wₖ,ₗ|
```

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

**Backprop with vectors:** for a gate z = f(x, y) where x has dimension D_x and y has D_y:
- z has dimension D_z
- Local gradients are Jacobian matrices: ∂z/∂x is [D_x × D_z], ∂z/∂y is [D_y × D_z]
- Downstream gradient ∂L/∂x = (∂z/∂x) · (∂L/∂z) — a matrix-vector multiply
- Loss L is always a scalar regardless of intermediate tensor dimensions

**Biological analogy:** A real neuron collects impulses via dendrites toward the cell body, then fires down the axon to presynaptic terminals. An artificial neuron computes: `f(Σᵢ wᵢxᵢ + b)` — inputs weighted by synaptic strengths, summed at the cell body, passed through an activation function, sent as output. The analogy is approximate but gives intuition for why the architecture is called a "neural" network.

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
