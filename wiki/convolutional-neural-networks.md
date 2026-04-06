# Convolutional Neural Networks

Convolutional Neural Networks (CNNs) are the dominant architecture for visual processing. Instead of looking at the entire image at once (like a fully-connected layer), CNNs use small **filters** that slide across the image, detecting local patterns. A CNN is a stack of convolutional layers interleaved with activation functions, pooling, and normalization layers.

## Source

- [[raw/03-stanford-cs231n/Stanford CS231N.md|raw/03-stanford-cs231n/Stanford CS231N.md]]
- [[raw/00-clippings/Spring 2025  Lecture 5 Image Classification with CNNs - YouTube.md|raw/00-clippings/Spring 2025  Lecture 5 Image Classification with CNNs - YouTube.md]]
- [[raw/00-clippings/(824) Stanford CS231N Deep Learning for Computer Vision  Spring 2025  Lecture 6 CNN Architectures - YouTube.md|raw/00-clippings/(824) Stanford CS231N Deep Learning for Computer Vision  Spring 2025  Lecture 6 CNN Architectures - YouTube.md]]

## Key Papers

- [ImageNet Classification with Deep Convolutional Neural Networks (AlexNet)](https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf) - the breakthrough paper that made deep CNNs the default vision architecture.
- [Very Deep Convolutional Networks for Large-Scale Image Recognition (VGG)](https://arxiv.org/pdf/1409.1556) - the paper that standardized stacked `3x3` convolutions.
- [Deep Residual Learning for Image Recognition (ResNet)](https://arxiv.org/pdf/1512.03385) - the decisive paper on skip connections for very deep CNNs.
- [Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification](https://arxiv.org/pdf/1502.01852) - the Kaiming-initialization paper referenced later in this page.

![AlexNet is the historical inflection point that turned CNNs into the dominant vision backbone.](../raw/03-stanford-cs231n/images/img_110.png)

*This architecture slide is worth keeping near the top because it anchors several later themes on the page: convolution stacks, pooling, fully connected heads, and the ImageNet-era design language that VGG and ResNet evolved from.*

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

**Historical milestone:** [ImageNet Classification with Deep Convolutional Neural Networks (AlexNet)](https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf) won ImageNet with a deep CNN and triggered the modern deep learning era. It achieved top-5 error of 15.3% vs. the prior year's 26.2%.

## Convolution Layer: Dimensions

A convolution layer takes a volume and produces a new volume via filters:

```
Input: 3 × 32 × 32
Filters: 6 filters, each 3 × 5 × 5
Output: 6 × 28 × 28 (one activation map per filter, stacked)
```

The filter's depth must match the input's depth (3 channels). The bias is a 6-dim vector (one per filter). The output is a 6 × 28 × 28 volume — 6 activation maps, each 28 × 28.

**Spatial dimension formula:**
- Input: W × W
- Filter: K × K, stride S, padding P
- Output: (W − K + 2P) / S + 1

Example without padding: 7 × 7 input, 3 × 3 filter → output is 5 × 5. **Problem: feature maps shrink with each layer** — padding solves this.

**Computation example:** input 3 × 32 × 32, 10 filters 5 × 5, stride 1, pad 2:
- Output size: 10 × 32 × 32 (padding preserves spatial size)
- Parameters: 10 × (3 × 5 × 5 + 1 bias) = 760 learnable parameters
- Multiply-add operations: 760 params × 10,240 outputs = **768K operations**

## VGGNet: Why 3×3 Filters?

[Very Deep Convolutional Networks for Large-Scale Image Recognition (VGG)](https://arxiv.org/pdf/1409.1556) uses stacked 3×3 conv layers exclusively:

- **Effective receptive field:** 3 stacked 3×3 conv layers have the same receptive field as one 7×7 layer
- **Fewer parameters:** 3 × (3² × C²) = 27C² vs. one 7² × C² = 49C² — for the same C channels, 3×3 stacks use 45% fewer parameters
- **More non-linearities:** 3 activation functions vs. 1 → more expressive capacity

VGG16 and VGG19 are the most common variants (16 or 19 weight layers). Both significantly outperform AlexNet on ImageNet.

## Normalization Layers

### Batch Normalization

Batch norm normalizes activations within a mini-batch to mean 0, variance 1, then learns scale (γ) and shift (β):
- Stabilizes training — reduces sensitivity to weight initialization
- Acts as a regularizer (implicit noise from mini-batch statistics)
- Enables training of much deeper networks
- Applied after the linear/conv layer, before the activation

### Layer Normalization

LayerNorm normalizes across the feature dimension (not the batch dimension):
- Input: N × D (N samples, D features)
- Statistics: μ, σ computed per sample → N × 1
- Learned params: γ, β → 1 × D (applied to each sample)
- Formula: `y = γ(x − μ) / σ + β`
- Preferred in transformers because it doesn't depend on batch size (Ba, Kiros, Hinton, 2016)

## Data Augmentation

Training images are randomly transformed to expand the effective dataset size and reduce overfitting:
- **Horizontal flips** — most common; works for most image classification tasks (cat facing left = same category as cat facing right)
- **Random crops** — sample different patches from the image at training time
- **Color jitter** — adjust brightness, contrast, saturation
- **Random scaling** — resize to different sizes before cropping

At test time, multiple augmented views of the same image are averaged (test-time augmentation / TTA).

## What Do Conv Filters Learn?

The first conv layer + ReLU block reduces the 3×32×32 input image to a 28×28 feature map. The linear classifier (weight matrix W) learns one template per class — each row of W, when viewed as an image, shows what the classifier "looks for":
- **Plane** — blue-gray gradient (sky + wings)
- **Car** — dark center with red sides (car body)
- **Bird** — feathered texture
- **Cat** — centered face template
- **Dog** — similar to cat but flatter
- **Ship** — blue bottom (water), light top

Limitation: **one template per class** cannot handle multimodal structure (e.g., red cars and blue cars are averaged together into a purple car template).

## ILSVRC Progress (2010–2017)

The ImageNet Large Scale Visual Recognition Challenge drove the deep learning revolution:

| Year | Model | Team | Top-5 Error |
|---|---|---|---|
| 2010 | — | Lin et al. | 28.2% |
| 2011 | — | Sanchez & Perronnin | 25.8% |
| 2012 | **AlexNet** | Krizhevsky, Sutskever, Hinton | **16.4%** ← breakthrough |
| 2013 | ZF Net | Zeiler & Fergus | 11.7% |
| 2014 | VGG | Simonyan & Zisserman | 7.3% |
| 2014 | GoogLeNet | Szegedy et al. | 6.7% |
| 2015 | **ResNet** | He et al. | **3.6%** |
| 2016 | — | Shao et al. | 3.0% |
| 2017 | SENet | Hu et al. | 2.3% |
| — | Human | Russakovsky et al. | 5.1% |

AlexNet (8 layers) in 2012 cut the error rate nearly in half compared to 2011 — the event that launched the modern deep learning era. ResNet (152 layers) surpassed human-level performance on this benchmark in 2015.

![ImageNet winners show the paper-driven jump from AlexNet to VGG, GoogLeNet, and ResNet.](../raw/03-stanford-cs231n/images/img_163.png)

*The pattern is the important part: benchmark progress was not smooth optimization, it came from architecture papers that changed how the field designed networks.*

## Pooling Layers

Pooling reduces spatial dimensions — standard max pooling:
- **Input:** C × H × W
- **Hyperparameters:** kernel size K, stride S, pooling function (max or average)
- **Output:** C × H' × W' where H' = (H − K) / S + 1
- **No learnable parameters** — fixed operation

**Common setting:** max pooling with K=2, S=2 → 2× spatial downsampling.

## Fully Connected Layers

A fully connected layer after the convolutional body:
- 32×32×3 image → flatten to **3072×1**
- Weight matrix W: 10 × 3072 (10 classes)
- Each row of W represents one class template
- Output activation[i] = dot product of row i of W with the 3072-dimensional input vector

## Activation Functions

Without activation functions, a stack of convolutional layers collapses to a single linear operation. Activations add non-linearity:

**Activation functions gallery:**
- **ReLU** max(0, x) — standard; zero for negatives, linear for positives
- **Leaky ReLU** max(0.1x, x) — small gradient for negatives; prevents dead neurons
- **ELU** — smooth negative region using exponential
- **GeLU** x·Φ(x) — smooth everywhere; main activation in transformers
- **Sigmoid** σ(x) = 1/(1+e⁻ˣ) — squashes to [0,1]; vanishing gradient at saturation
- **Tanh** (eˣ−e⁻ˣ)/(eˣ+e⁻ˣ) — squashes to [-1,1]; used in RNNs
- **SiLU** x·σ(x) — also called Swish; smooth, gated variant

**Sigmoid:** σ(x) = 1/(1 + e⁻ˣ)
- Squashes numbers to [0, 1]
- Historically popular as a "firing rate" analogy
- **Key problem:** many layers of sigmoid → smaller and smaller gradients (saturation in flat regions near 0 and 1 kills gradient flow)

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

![ResNet reframes depth as learning residual change on top of an identity path.](../raw/03-stanford-cs231n/images/img_174.png)

*This figure captures the core ResNet paper insight more directly than a paragraph: the deeper model should only need to learn the residual difference from identity, not relearn the whole mapping from scratch.*

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
