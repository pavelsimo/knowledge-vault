# Computer Vision

Computer vision is the field of teaching machines to interpret and understand images and video. It encompasses a range of tasks from basic image classification to complex segmentation and 3D understanding. This topic synthesizes content from Stanford CS231N and Hugging Face applied examples.

## Sources

- `raw/03-stanford-cs231n/Stanford CS231N.md`
- `raw/01-open-source-models-hugging-face/08_object_detection.py`
- `raw/01-open-source-models-hugging-face/09_segmentation_mask.py`
- `raw/01-open-source-models-hugging-face/10-depth-estimation.py`
- `raw/01-open-source-models-hugging-face/11-image-retrieval.py`
- `raw/01-open-source-models-hugging-face/12-image-captioning.py`

## Image Classification

Image classification assigns a single label from a fixed set of categories to an image (e.g., "cat" or "dog").

### The Semantic Gap

**The core problem:** an image is a tensor of integers between [0, 255]. A cat photo is stored as an 800 × 600 × 3 array of numbers — the computer sees nothing but those numbers. A human looking at the same photo instantly recognizes a cat. This gap between the human semantic understanding and the machine's pixel representation is the central challenge of computer vision.

### Why It's Hard: The Challenges

| Challenge | Description |
|-----------|-------------|
| **Semantic gap** | Humans understand meaning; machines see raw pixel values (an 800×600×3 tensor) |
| **Viewpoint variation** | Camera movement changes ALL pixels, even for the same object |
| **Illumination** | RGB pixel values are a function of surface material, color, AND light source — same cat looks different under different lighting |
| **Background clutter** | Other objects in the background make it harder to clearly see the target object |
| **Occlusion** | Part of the object is hidden |
| **Deformation** | Object appears in unusual shapes or poses |
| **Intra-class variation** | Objects in the same category can look very different |
| **Context** | Surroundings influence how an object is recognized |

### Algorithmic vs Data-Driven Approach

**Algorithmic (hand-crafted rules):**
- Detect edges → detect corners → combine into object rules
- Problem: doesn't scale; must repeat for every new class; rules too simple to capture real variations

**Data-driven approach:**
```python
def train(images, labels):
    # Machine learning!
    return model

def predict(model, test_images):
    # Use model to predict labels
    return test_labels
```
The model learns features automatically from examples — training data with labels for airplane, automobile, bird, cat, deer, etc. Foundation of modern deep learning.

## Distance Metrics for Image Comparison

Used in K-Nearest Neighbors (KNN) classification:

- **L1 distance (Manhattan):** sum of absolute pixel differences
- **L2 distance (Euclidean):** square root of sum of squared differences

### KNN Classifier

- Finds K closest training images to a test image
- Assigns the majority class label among those K neighbors
- Training: O(1) — just store data
- Prediction: O(n) — must compare against all training examples
- **Not used in practice** for images: too slow at inference, distance metrics behave poorly in high-dimensional pixel space

## Linear Classifier

A linear classifier makes predictions using: `f(x; W) = Wx + b`

- `x` = image flattened into a vector (e.g., 32×32×3 = 3072 numbers)
- `W` = weight matrix (learned parameters)
- `b` = bias vector
- Output = score for each class

**Geometric interpretation:** each row of W acts as a class template; the dot product measures how similar the image is to that template.

**Hard cases for linear classifiers:** non-linear decision boundaries, circular data, multimodal class distributions — solved by stacking layers into neural networks.

## Segmentation Mask Generation

Pixel-accurate object outlining without necessarily identifying the class (class-agnostic segmentation).

- **Model:** `Zigeng/SlimSAM-uniform-77` (based on Segment Anything Model)
- SAM outputs **3 candidate masks** per prompt
- Can be prompted with a single point, bounding box, or text
- Paper: [0.1% Data Makes Segment Anything Slim](https://arxiv.org/pdf/2312.05284)

## Depth Estimation

Estimating the distance of objects in an image from the camera — common in autonomous driving and robotics.

- **Model:** `Intel/dpt-hybrid-midas`
- **DPT** = Dense Prediction Transformer
- Paper: [Vision Transformers for Dense Prediction](https://arxiv.org/pdf/2103.13413)

## Related Topics

- [[object-detection]] — detecting and localizing multiple objects in an image
- [[convolutional-neural-networks]] — the dominant architecture for vision
- [[multimodal-models]] — models combining vision with text
- [[neural-networks]] — foundational building blocks
- [[attention-transformers]] — ViT: transformers applied to vision
- [[hugging-face]] — pretrained models for vision tasks
