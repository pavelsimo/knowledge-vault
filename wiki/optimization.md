# Optimization

Optimization in machine learning refers to the algorithms that iteratively adjust model weights to minimize the loss function. All modern deep learning optimizers are variants of stochastic gradient descent (SGD).

## Source

- [[raw/03-stanford-cs231n/Stanford CS231N.md|raw/03-stanford-cs231n/Stanford CS231N.md]]

## Gradient Descent

**Gradient descent** follows the negative gradient of the loss to reach a minimum:

```
w ← w - η · ∇L(w)
```

- `η` (eta) = **learning rate** — the step size
- Too small: very slow convergence
- Too large: overshoots, bounces around, diverges

## Stochastic Gradient Descent (SGD)

Full batch gradient descent computes the gradient over ALL N examples each step:
```
L(W) = (1/N) Σᵢ Lᵢ(xᵢ, yᵢ, W) + λR(W)
∇_W L(W) = (1/N) Σᵢ ∇_W Lᵢ(xᵢ, yᵢ, W) + λ∇_W R(W)
```
"Full sum expensive when N is large!"

**SGD** computes the gradient on a **random mini-batch** each step (32/64/128 common):
```python
# Vanilla Minibatch Gradient Descent
while True:
    data_batch = sample_training_data(data, 256)  # sample 256 examples
    weights_grad = evaluate_gradient(loss_fun, data_batch, weights)
    weights += - step_size * weights_grad          # perform parameter update
```
- "Stochastic" = random (each mini-batch is a random sample)
- The gradient is a **noisy estimate** of the true gradient
- Why it works: the noise can help escape poor local minima and improve generalization
- All modern deep learning uses SGD variants

**Learning rate behavior:** visualizing train loss curves:
- **Very high LR:** loss explodes or oscillates wildly
- **High LR:** converges fast but to worse final value
- **Good LR:** smooth convergence to best minimum
- **Low LR:** converges slowly but steadily toward good solution

"In reality, all of these could be good learning rates" — the best choice depends on the schedule. Train/Val accuracy both still rising → need to train longer (underfitting).

### Problems with Vanilla SGD

1. **Slow progress on flat dimensions:** oscillates rapidly along steep dimensions, crawls along shallow ones
2. **Getting stuck:** zero gradient at saddle points causes convergence to stop
3. **Noisy updates:** mini-batch gradients are noisy → messy, erratic optimization path

## SGD with Momentum

SGD computes `x_{t+1} = x_t - α∇f(x_t)`. Momentum keeps a velocity that continues moving in the general direction of previous iterations:

```
SGD:              x_{t+1} = x_t - α∇f(x_t)

SGD + Momentum:   v_{t+1} = ρv_t + ∇f(x_t)
                  x_{t+1} = x_t - αv_{t+1}
```

Where:
- ρ = "rho" gives the momentum; typically ρ = 0.9 or 0.99
- v = velocity (running mean of gradients)
- "Build up velocity as a running mean of gradients"

Benefits:
- Builds speed along consistent directions (accelerates on flat surfaces)
- Dampens oscillations along steep/noisy directions
- Helps escape saddle points

(Sutskever et al., "On the importance of initialization and momentum in deep learning", ICML 2013)

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

## Practical Optimizer Advice

From CS231N slides:
- **Adam(W)** is a good default choice in many cases; it often works fine even with a constant learning rate
- **SGD + Momentum** can outperform Adam but may require more tuning of LR and schedule
- If you can afford full batch updates, look beyond 1st order optimization (2nd order and beyond)

**Historical recognition:** Adam won the ICLR 2025 "Test of Time" award — "Adam revolutionized neural network training, enabling significantly faster convergence and more stable training across a wide variety of architectures and tasks." (Kingma & Ba, 2015, 42K citations)

In practice, AdamW with cosine decay + warmup is the standard recipe for transformer training.

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
