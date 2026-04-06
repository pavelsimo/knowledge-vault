# Object Detection

Object detection is the task of identifying **what** objects are in an image and **where** they are (bounding boxes + class labels). It extends image classification from one label for the whole image to multiple localized predictions.

## Source

- `raw/03-stanford-cs231n/Stanford CS231N.md`
- `raw/01-open-source-models-hugging-face/08_object_detection.py`

## Task Definition

Given an image, output:
- A set of **bounding boxes** (x, y, width, height)
- A **class label** for each box
- A **confidence score** for each prediction

## Two-Stage Detectors (RCNN Family)

Two-stage detectors first generate region proposals, then classify each proposal.

### R-CNN (Region-based CNN)
1. Use a region proposal algorithm (Selective Search) to generate ~2000 candidate regions
2. Warp each region to a fixed size
3. Pass each through a CNN to extract features
4. Classify with SVM, refine bounding box with regression
- **Problem:** very slow (2000 forward passes per image)

### Fast R-CNN
- Process the entire image with CNN once → shared feature map
- Project region proposals onto the feature map (ROI pooling)
- Classify all regions from the shared features
- Much faster than R-CNN

### Faster R-CNN
- Replace Selective Search with a **Region Proposal Network (RPN)** — also a CNN
- End-to-end trainable
- Still the foundation for many modern two-stage detectors

## Single-Stage Detectors (YOLO / SSD / RetinaNet)

Single-stage detectors predict bounding boxes and classes directly in one pass — faster but historically less accurate than two-stage.

### YOLO (You Only Look Once)

Grid-based end-to-end detection:
- Divide image into S×S grid cells
- Each cell predicts B bounding boxes and C class probabilities
- One forward pass → all predictions simultaneously
- Trade speed for some accuracy on small objects

Notable versions: YOLOv2/YOLO9000, YOLOv3, and many subsequent iterations.

### SSD (Single Shot MultiBox Detector)
- Multi-scale anchor boxes — better at small objects than original YOLO
- Uses feature maps at multiple scales

### RetinaNet
- Introduces **Focal Loss** to address class imbalance (many easy background examples dominate training)
- Achieves two-stage accuracy at single-stage speed

## DETR (Detection Transformer)

**[Facebook DETR](https://huggingface.co/facebook/detr-resnet-50)** was the first object detector to frame detection as a **direct set prediction problem** using a Transformer:
- No anchor boxes, no non-maximum suppression (NMS)
- CNN backbone extracts features → Transformer encoder-decoder predicts object set
- Bipartite matching loss during training
- Simpler pipeline but slower training convergence than RCNN

```python
from transformers import pipeline
detector = pipeline("object-detection", model="facebook/detr-resnet-50")
result = detector(image)
```

## Anchor Boxes

Most non-DETR detectors use **anchor boxes** — predefined bounding box shapes at each spatial location:
- The model predicts offsets and class scores relative to anchors
- Different anchors cover different aspect ratios and scales
- DETR eliminates the need for anchors entirely

## Evaluation Metric: mAP

**Mean Average Precision (mAP)** is the standard evaluation metric:
- Compute precision-recall curve for each class
- Average precision (AP) = area under the curve
- mAP = mean AP across all classes

## Related Topics

- [[computer-vision]] — broader vision tasks (segmentation, depth estimation)
- [[convolutional-neural-networks]] — CNN backbones used in most detectors
- [[attention-transformers]] — transformer-based detectors (DETR, DINO)
- [[mlops]] — monitoring object detection models in production
- [[hugging-face]] — pretrained detection models
