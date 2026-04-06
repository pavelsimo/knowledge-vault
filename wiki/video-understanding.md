# Video Understanding

Video understanding extends computer vision from still images to sequences of frames. The key challenge is modeling both spatial appearance and temporal dynamics efficiently, since video data is enormous compared to images.

## Source

- `raw/03-stanford-cs231n/Stanford CS231N.md`

## Video as Data

Video = 2D images + time

**Scale of uncompressed video (3 bytes/pixel):**
| Resolution | Data per minute |
|-----------|----------------|
| SD (640×480) | ~1.5 GB/min |
| HD (1920×1080) | ~10 GB/min |

**Practical solution:** train on short clips at low fps and low spatial resolution (e.g., 3.2s at 5fps = 588 KB).

**In video classification**, actions are classified rather than object categories (e.g., "swimming" vs "playing guitar").

## Video Classification Approaches

### 1. Single Frame CNN

Classify each frame independently using a 2D image CNN, then pick the most common prediction. No temporal modeling whatsoever — a simple baseline.

### 2. Late Fusion

Process each frame independently with a 2D CNN, then combine features at the end:

```
T frames → [same 2D CNN per frame] → stack T feature maps → flatten → MLP → class scores
```

**Strengths:** simple; reuses strong ImageNet-pretrained CNNs.

**Weaknesses:** no real motion modeling; temporal order mostly ignored; large FC layers.

Paper: [Large-scale Video Classification with Convolutional Neural Networks](https://arxiv.org/pdf/1406.2199)

### 3. Early Fusion

Fuse time at the very first convolution by stacking frames along the channel dimension:

```
T × 3 × H × W  →  reshape to  (3T) × H × W  →  standard 2D CNN
```

**Strengths:** motion captured at pixel level from the start.

**Weaknesses:** temporal modeling happens only once; later layers lose temporal awareness.

**Key limitation:** early fusion lacks **temporal shift-invariance** — it learns *when* something happens, not *what* happens regardless of timing.

### 4. 3D CNN

**2D Conv (Early Fusion) vs. 3D Conv comparison:**

| | 2D Conv (Early Fusion) | 3D Conv |
|---|---|---|
| Input | C_in × T × H × W (3D grid with C_in-dim feat at each point) | C_in × T × H × W |
| Weight | C_out × C_in × 1 × 3 × 3 (no temporal kernel!) | C_out × C_in × T × 3 × 3 |
| Slide over | x and y | x, y, AND time |
| Output | C_out × H × W (2D grid) | C_out × H × W (2D grid) |
| Temporal issue | No temporal shift-invariance — learns separate filters for same motion at different times in clip | Temporal shift-invariant |

Treat time as a first-class dimension alongside height and width:
```
Kernel: (kT × kH × kW)
Input: 3 × T × H × W (e.g., 3 × 16 × 224 × 224)
```

**Strengths:** explicit motion modeling; learns temporal patterns hierarchically; temporal shift-invariant.

**Weaknesses:** very expensive; needs large datasets; harder to pretrain.

Paper: [3D Convolutional Neural Networks for Human Action Recognition](https://arxiv.org/abs/1412.0767)

### 5. Two-Stream Networks

Separate appearance and motion into two parallel CNNs:
- **Spatial stream:** RGB frames → 2D CNN
- **Temporal stream:** optical flow → 2D CNN
- Late fusion combines both predictions

Inspired by neuroscience: humans are excellent at recognizing motion from minimal information (just key points on a skeleton).

Paper: [Two-Stream Convolutional Networks for Action Recognition in Videos](https://arxiv.org/pdf/1406.2199)

### 6. 3D CNN with Inflated Weights (I3D)

Reuse pretrained 2D ImageNet weights in a 3D CNN by "inflating" 2D filters to 3D:
- Start by treating all frames equally
- Let training refine the temporal dimension
- Initialize from strong 2D pretrained weights → faster convergence

Paper: [Quo Vadis, Action Recognition? A New Model and the Kinetics Dataset](https://arxiv.org/pdf/1705.07750)

### Comparison Table

| Method | Motion Modeling | Complexity | Notes |
|--------|----------------|------------|-------|
| Late Fusion (FC) | None | High params | Simple baseline |
| Late Fusion (Pool) | None | Low | Efficient |
| Early Fusion | Weak (once) | Medium | Short motion |
| 3D CNN | Strong | Very high | Best classical CNN |
| Two-Stream | Strong | Medium | Appearance + motion |

## Video Transformers

Self-attention naturally extends to video since it has no locality bias:
- [Is Space-Time Attention All You Need for Video Understanding? (TimeSformer)](https://arxiv.org/pdf/2102.05095)
- [ViViT: A Video Vision Transformer](https://arxiv.org/pdf/2103.15691)
- [Video Transformer Network](https://arxiv.org/pdf/2102.00719)

## Temporal Action Localization

Given a long **untrimmed** video, identify when (start/end timestamps) different actions occur.

Paper: [Rethinking the Faster R-CNN Architecture for Temporal Action Localization](https://arxiv.org/pdf/1804.07667)

## Modeling Long-Term Temporal Structure with RNNs

To model temporal structure beyond what a single CNN clip can capture, use CNN feature extractors feeding into an RNN:

```
Frame₁  Frame₂  Frame₃  Frame₄  Frame₅
  ↓        ↓        ↓       ↓       ↓
 CNN      CNN      CNN     CNN     CNN    (2D or 3D, sometimes frozen as feature extractor)
  ↓        ↓        ↓       ↓       ↓
 LSTM ←→ LSTM ←→ LSTM ←→ LSTM ←→ LSTM   (bidirectional, captures long-range dependencies)
  ↓
Classification
```

Key note: sometimes the CNN is not backpropagated through (to save memory). Pretrain the CNN on ImageNet or Kinetics, then use it as a fixed feature extractor, and only train the RNN.

Papers: Baccouche et al., "Sequential Deep Learning for Human Action Recognition" (2011); Donahue et al., "Long-term Recurrent Convolutional Networks" (CVPR 2015)

## Spatio-Temporal Detection

Given a long untrimmed video, detect all people in both space (where) and time (when) and classify their activities.

**Example from AVA dataset:** given an untrimmed clip, simultaneously detect:
- A person clinking glasses → "drink"
- Two people → "open → close" interaction
- A person reaching → "grab (a person) → hug"
- A person looking at phone → "answer phone"

Dataset: [AVA: A Video Dataset of Spatio-temporally Localized Atomic Visual Actions](https://arxiv.org/pdf/1705.08421)

## Audio-Visual Video Understanding

Video is multimodal — images come with audio. Tasks include:
- **Audio source separation:** separate instrument sounds in a music ensemble
- **Visually-guided separation:** use speaker's lip movements to isolate their voice in a crowd ("cocktail party problem")
- **Video + LLMs:** Video-LLaVA, Video-ChatGPT, VideoLLaMA-3 — connect video understanding with language models

Papers:
- [Looking to Listen at the Cocktail Party](https://arxiv.org/pdf/1804.03619)
- [Video-LLaVA: Learning United Visual Representations by Alignment Before Projection](https://arxiv.org/pdf/2311.10122)

## Datasets

| Dataset | Content | Scale |
|---------|---------|-------|
| [Sports-1M](https://github.com/gtoderici/sports-1m-dataset) | Sports videos | 1M clips |
| [UCF-101](https://www.kaggle.com/datasets/matthewjansen/ucf101-action-recognition) | Human actions | 101 classes |
| [Kinetics-400](https://www.kaggle.com/datasets/ipythonx/k4testset) | Human actions | 400 classes |
| [AVA](http://research.google.com/ava/) | Spatio-temporal actions | Dense annotation |

## Related Topics

- [[convolutional-neural-networks]] — 2D/3D CNN architectures for video
- [[recurrent-neural-networks]] — RNNs for temporal modeling in video
- [[attention-transformers]] — video transformers (ViViT, TimeSformer)
- [[self-supervised-learning]] — video colorization as a pretext task for tracking
- [[computer-vision]] — image-level tasks extended to video
