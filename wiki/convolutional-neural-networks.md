# Convolutional Neural Networks

Convolutional Neural Networks (CNNs) are the dominant architecture for visual processing. Instead of looking at the entire image at once (like a fully-connected layer), CNNs use small **filters** that slide across the image, detecting local patterns. A CNN is a stack of convolutional layers interleaved with activation functions, pooling, and normalization layers.

## Source

- `raw/03-stanford-cs231n/Stanford CS231N.md`

## Why CNNs?

A fully-connected layer on an image:
- Flattens the entire image (e.g., 32×32×3 = 3072 inputs)
- Every pixel connected to every neuron → huge number of parameters
- Ignores spatial structure

A convolutional layer:
- Uses small **filters** (e.g., 3×3 or 5×5) that slide across the image
- Each filter detects one type of local feature (edge, corner, texture)
- Parameters are **shared** across all positions → vastly fewer parameters
- Output is a **feature map** — one channel per filter

> "Convolutional" comes from the mathematical convolution operation — folding two functions together.

## Architecture

A typical CNN: `Input → [Conv → ReLU]* → Pool → [FC]* → Softmax`

All the nodes in a CNN are neurons — they just have different connectivity patterns.

## Activation Functions

Without activation functions, a stack of convolutional layers collapses to a single linear operation. Activations add non-linearity:

| Activation | Notes |
|------------|-------|
| **ReLU** | `max(0, x)` — standard for CNNs; fast, sparse |
| **Leaky ReLU** | Allows small negative values; fixes dying neuron problem |
| **ELU** | Smooth negative region |
| **SELU** | Self-normalizing |
| **GeLU** | `x · Φ(x)` — main activation in transformers today |
| **Sigmoid** | Squashes to [0,1]; only used in output for binary classification |
| **Tanh** | Squashes to [-1,1]; used in RNNs |

## Dropout

Dropout is a regularization technique that randomly zeros out neurons during training:
- Each neuron is dropped with probability p (typically 0.5)
- Forces the network to learn redundant representations
- Prevents co-adaptation: neurons cannot rely on specific other neurons always being present
- At inference, all neurons are active but outputs are scaled

## Batch Normalization

Batch norm normalizes activations within a mini-batch to have mean 0 and variance 1, then learns scale and shift parameters:
- Stabilizes training — reduces sensitivity to weight initialization
- Acts as a regularizer (implicit noise from mini-batch statistics)
- Enables training of much deeper networks
- Applied after the linear/conv layer, before the activation

## Weight Initialization

Improper initialization causes **vanishing** or **exploding activations**:

- **Too small weights:** activations shrink toward zero in deep layers → gradients also vanish → model can't learn
- **Too large weights:** activations explode → unstable training

**Goal:** initialize so that activations stay at the same scale across layers.

Solutions:
- **Xavier/Glorot initialization** — for tanh/sigmoid activations
- **He/Kaiming initialization** — for ReLU activations (accounts for ~50% of neurons being zeroed)

## ResNet (Residual Networks)

Deep networks suffer from degradation — more layers → worse training performance (not just overfitting, but underfitting). ResNet solves this with **skip connections**:

```
output = F(x) + x
```

Each block only needs to learn what **changed** (the residual), not everything from scratch:
- Gradients flow directly back through skip connections → no vanishing gradient
- Enables training of networks with hundreds of layers
- Skip connections behave similarly to LSTMs' cell state highways

## Transfer Learning

Pretrained CNNs (ResNet, VGG, EfficientNet) trained on ImageNet are reused for new tasks:
- Freeze earlier layers (general features: edges, textures)
- Fine-tune later layers on new task-specific data
- Dramatically reduces training data and compute needed

## Related Topics

- [[neural-networks]] — loss functions, regularization, backpropagation
- [[optimization]] — SGD, Adam, and other optimizers used to train CNNs
- [[computer-vision]] — tasks CNNs are applied to (classification, segmentation, depth)
- [[object-detection]] — CNN-based detection architectures (RCNN, YOLO)
- [[attention-transformers]] — ViT: replacing convolutions with attention
