# Optimization

Optimization in machine learning refers to the algorithms that iteratively adjust model weights to minimize the loss function. All modern deep learning optimizers are variants of stochastic gradient descent (SGD).

## Source

- `raw/03-stanford-cs231n/Stanford CS231N.md`

## Gradient Descent

**Gradient descent** follows the negative gradient of the loss to reach a minimum:

```
w ← w - η · ∇L(w)
```

- `η` (eta) = **learning rate** — the step size
- Too small: very slow convergence
- Too large: overshoots, bounces around, diverges

## Stochastic Gradient Descent (SGD)

Standard gradient descent computes the gradient on **all training data** — too expensive for large datasets.

**SGD** computes the gradient on a **random mini-batch** each step:
- "Stochastic" = random (each mini-batch is a random sample)
- The gradient is a **noisy estimate** of the true gradient
- Why it works: the noise can help escape poor local minima and improve generalization
- All modern deep learning uses SGD variants

### Problems with Vanilla SGD

1. **Slow progress on flat dimensions:** oscillates rapidly along steep dimensions, crawls along shallow ones
2. **Getting stuck:** zero gradient at saddle points causes convergence to stop
3. **Noisy updates:** mini-batch gradients are noisy → messy, erratic optimization path

## SGD with Momentum

Momentum adds a velocity term that accumulates gradients over time:

```
v ← β·v - η·∇L(w)
w ← w + v
```

Benefits:
- Builds speed along consistent directions (accelerates on flat surfaces)
- Dampens oscillations along steep/noisy directions
- Helps escape saddle points

## RMSProp

Proposed by Geoffrey Hinton. Maintains a per-parameter running average of squared gradients and normalizes the update by it:

- Slows down learning for parameters with large gradients
- Speeds up learning for parameters with small gradients
- Adapts the effective learning rate per parameter

## Adam (Adaptive Moment Estimation)

Adam = **Momentum + RMSProp**, with bias correction for the first few steps.

```python
# Pseudocode
m = β₁·m + (1-β₁)·grad          # first moment (momentum)
v = β₂·v + (1-β₂)·grad²         # second moment (RMSProp)
m_hat = m / (1 - β₁ᵗ)           # bias correction
v_hat = v / (1 - β₂ᵗ)           # bias correction
w = w - η · m_hat / (√v_hat + ε)
```

- `β₁ ≈ 0.9` — "where we were heading" (90% memory of past gradients)
- `β₂ ≈ 0.999` — squared gradient smoothing
- Bias correction prevents underestimates in early training steps
- **Most widely used optimizer in deep learning**

## AdamW

AdamW fixes a subtle bug in Adam: standard Adam applies weight decay **inside** the gradient update, which interacts with the momentum/RMS scaling and distorts it.

| Optimizer | Weight Decay Application |
|-----------|--------------------------|
| Adam | Applied inside gradient (distorted by moment estimates) |
| AdamW | Applied outside gradient (clean, correct L2 regularization) |

```
# AdamW adds this step after the Adam update:
w ← w - η · λ · w    # pure weight decay, independent of gradients
```

AdamW is the **preferred optimizer** for training transformers and large models.

## Weight Decay

Weight decay shrinks weights slightly on every update:

```
w ← w - η · gradient - η · λ · w
```

- Equivalent to **L2 regularization** in the loss function
- Keeps weights small → simpler model → better generalization
- Prevents exploding weights

## Learning Rate Schedules

The learning rate doesn't have to be constant. Common strategies:

- **Step decay:** reduce by factor (e.g., ×0.1) every N epochs
- **Cosine annealing:** smoothly reduce following a cosine curve
- **Warm-up + decay:** start small, ramp up, then decay (used in transformer training)
- **Cyclical learning rates:** oscillate between bounds to escape local minima

## Second-Order Optimization (Why We Don't Use It)

Second-order methods (e.g., Newton's Method) use the **Hessian** (curvature information):
- Can jump directly to the minimum in fewer steps
- No learning rate tuning needed

**Why not used in deep learning:**
- The Hessian is a N×N matrix where N = number of parameters
- 100K parameters → 10¹⁰ elements in the Hessian
- GPT-3: 175B parameters → Hessian is astronomically large
- Computing, storing, and inverting it is completely infeasible

## Optimizer Summary

| Optimizer | Analogy |
|-----------|---------|
| SGD | Reacts immediately to new gradient |
| Momentum | Remembers past gradients (builds velocity) |
| RMSProp | Slows down when gradients become too large |
| Adam | Combines memory + per-parameter scaling |
| AdamW | Adam with correct weight decay |

## Related Topics

- [[neural-networks]] — loss functions that optimizers minimize
- [[convolutional-neural-networks]] — deep networks trained with these optimizers
- [[attention-transformers]] — transformers typically use AdamW with warm-up scheduling
