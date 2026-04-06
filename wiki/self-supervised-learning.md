# Self-Supervised Learning

Self-supervised learning trains neural networks on unlabeled data by auto-generating supervision signals from the data itself. The model first solves a "pretext task" (not the real goal) which forces it to learn rich, transferable visual representations. Those representations are then fine-tuned on small labeled datasets for the real task.

## Source

- `raw/03-stanford-cs231n/Stanford CS231N.md`

## Why Self-Supervised Learning?

Supervised learning requires massive labeled datasets — expensive, incomplete, and task-specific. Self-supervised learning asks: **can the model learn useful representations from raw data alone?**

- No human annotation required
- The data supervises itself via transformations you control
- Learn representations that transfer broadly to many downstream tasks

## Learning Paradigms

| Paradigm | Labels | Objective | Example |
|----------|--------|-----------|---------|
| **Supervised** | All labeled | Task loss (cross-entropy) | ImageNet classification |
| **Unsupervised** | None | Structure (clustering, density) | K-means, PCA |
| **Self-supervised** | None (auto-generated) | Pretext task loss | Predict rotation, masked patches |
| **Semi-supervised** | Some labeled + many unlabeled | Task + auxiliary loss | SSL pretraining + fine-tune on few labels |

## Pretext Tasks

A pretext task is a made-up task used as an "excuse" to force the network to learn useful visual structure. The real goal is always good representations, not solving the pretext task.

### Predict Image Rotations

Train to recognize 0°, 90°, 180°, 270° rotations of an image. To predict rotation, the model must understand object orientation and semantics.

Paper: [Unsupervised Representation Learning by Predicting Image Rotations](https://arxiv.org/pdf/1803.07728)

### Predict Relative Patch Positions

Sample two patches from an image; predict the spatial relationship (above, below-left, etc.) between them. Forces the model to learn object parts and spatial layout.

Paper: [Unsupervised Visual Representation Learning by Context Prediction](https://arxiv.org/pdf/1505.05192)

### Solve Jigsaw Puzzles

Shuffle image patches and train the model to predict the correct permutation. Forces learning of object parts, spatial layout, and global structure.

Paper: [Unsupervised Learning of Visual Representations by Solving Jigsaw Puzzles](https://arxiv.org/pdf/1603.09246)

### Predict Missing Pixels (Image Inpainting)

Mask a region of the image and train the model to predict the missing pixels from context. Requires understanding of scene semantics and object appearance.

Paper: [Context Encoders: Feature Learning by Inpainting](https://arxiv.org/pdf/1604.07379)

### Image Colorization / Split-Brain Autoencoder

Train on grayscale images to predict the color channels. Forces the model to understand what objects look like — you can't color a banana without knowing it's a banana.

**Split-brain autoencoder:** split the image into two cross-channel prediction tasks:
- F₁: predict one subset of color channels from the rest
- F₂: predict the remaining channels
Both sub-networks must learn good representations since neither can see all channels.

Papers:
- [Colorful Image Colorization](https://arxiv.org/pdf/1603.08511)
- [Split-Brain Autoencoders: Unsupervised Learning by Cross-Channel Prediction](https://arxiv.org/pdf/1611.09842)

### Video Colorization → Tracking

Train on grayscale video to colorize frames consistently over time. To maintain consistent colors, the model must track objects frame-to-frame — implicitly learning tracking without any tracking labels.

**Mechanism:** uses an attention mechanism where each target pixel borrows color from the most similar reference frame pixel (via dot-product similarity + softmax).

Paper: [Tracking Emerges by Colorizing Videos](https://arxiv.org/pdf/1806.09594)

### Masked Autoencoder (MAE)

Mask 50–75% of image patches (at random) and train a ViT to reconstruct the missing patches from visible patches only. The high masking ratio forces the model to understand global image structure, not just fill in local texture.

- Architecture: **asymmetric** encoder-decoder
  - Encoder: processes only visible (unmasked) patches — sees far fewer tokens than full image
  - Decoder: merges encoder outputs with learned mask tokens (placed in previously masked positions), adds positional encodings, uses transformer blocks followed by linear projection for pixel reconstruction
  - The decoder is **not used post-training** — only the encoder is fine-tuned downstream
- The asymmetric design means the encoder and decoder can be designed independently; unlike traditional AEs or U-Net, they are not tightly coupled
- No labels — fully self-supervised
- Strong results that match or exceed supervised pretraining

Paper: [Masked Autoencoders Are Scalable Vision Learners](https://arxiv.org/pdf/2111.06377)

## Contrastive Representation Learning

Contrastive learning trains a model to:
- Pull representations of **the same object** (different augmentations) **together**
- Push representations of **different objects** **apart**

**Key concept — invariance:** the model learns which transformations should NOT change the identity of an image (crops, color shifts, rotations, blur → still the same cat).

### Downstream Task Setup

Once pretraining is complete, the learned representation is used for labeled tasks:
```
Dataset (with labels) → Encoder → Learned Representation → FC layer → Labels
                                   (frozen or fine-tuned)  (trained)
```
Labels are automatically generated from data structure during pretraining. The encoder learns general visual features; the small FC head adapts to the specific downstream task.

### SimCLR

SimCLR = Simple Contrastive Learning of Visual Representations. The main algorithm:
1. Sample a minibatch of N images from dataset
2. Apply two augmentation functions t, t' from family T to each image → N pairs
3. For each pair, encode with shared encoder f(·) → representations h, h⁺
4. Project to latent space with projection head g(·) → z, z⁺
5. Compute **InfoNCE loss** using all other 2(N−1) examples as negatives

Key: use ALL non-positive samples in the batch as X negatives — as X grows the contrastive task gets harder and representations get richer.

Paper: [A Simple Framework for Contrastive Learning of Visual Representations](https://arxiv.org/pdf/2002.05709)

### MoCo (Momentum Contrast)

MoCo decouples the number of negatives from the batch size using:
- A **memory queue** of past encoded keys (many negatives without giant batches)
- A **momentum encoder** (slowly updated copy of the online encoder) for stable key representations

Paper: [Improved Baselines with Momentum Contrastive Learning (MoCo v2)](https://arxiv.org/pdf/2003.04297)

### InfoNCE Loss

Derived from mutual information maximization. Given a query q and its positive key k⁺ among N-1 negative keys:

```
L = -log [exp(q·k⁺/τ) / Σ exp(q·kᵢ/τ)]
```

Papers:
- [Representation Learning with Contrastive Predictive Coding](https://arxiv.org/pdf/1807.03748)
- [On Variational Bounds of Mutual Information](https://arxiv.org/pdf/1905.06922)

### DINO

DINO uses **self-distillation without labels**:
- Student network: processes local crops → makes predictions
- Teacher network: processes global view → provides targets (EMA of student)
- No explicit negatives; no contrastive loss; just consistency between views

DINO produces strongly **object-centric** attention maps — the model learns to separate foreground from background without any supervision.

Paper: [Emerging Properties in Self-Supervised Vision Transformers](https://arxiv.org/pdf/2104.14294)

### DINOv2

Scales DINO with curated data (hundreds of millions of images), larger ViT backbones, and better training recipes. Produces a **general-purpose vision encoder** that works out-of-the-box for classification, segmentation, depth estimation, and retrieval.

Paper: [DINOv2: Emergent Abilities in Self-Supervised Vision Transformers](https://hal.science/hal-04376640v2/file/CVPR_2023_dinov2%20%284%29.pdf)

## Contrastive Predictive Coding (CPC)

Trains a model to predict **future representations** in a sequence (audio, image patches, video frames) using contrastive learning. Forces the model to learn high-level temporal structure rather than low-level pixel details.

Paper: [Representation Learning with Contrastive Predictive Coding](https://arxiv.org/pdf/1807.03748)

## Key Insight: Why It Works

> Supervised learning: "Here is the answer, memorize it."
>
> Contrastive self-supervised learning: "Figure out what stays the same when I mess with the input."

Self-supervised pretraining is most valuable when labeled data is limited. As labeled data grows, its advantage decreases — but it remains a powerful initialization.

## Related Topics

- [[convolutional-neural-networks]] — CNN encoders used in SimCLR, MoCo
- [[attention-transformers]] — ViT backbone in MAE, DINO, DINOv2
- [[generative-models]] — autoencoders and VAEs as related self-supervised approaches
- [[video-understanding]] — video colorization as temporal pretext task
- [[multimodal-models]] — CLIP/CLAP also use contrastive learning
