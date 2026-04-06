# MLOps (Machine Learning Engineering for Production)

MLOps covers the practices, tools, and workflows for deploying, monitoring, and maintaining machine learning models in production. A model that performs well in the lab can degrade silently in the real world — MLOps provides the discipline to detect and respond to that.

## Source

- `raw/04-machine-learning-engineering-for-production-mlops/Machine Learning Engineering for Production (MLOps).md`
- Course: https://www.youtube.com/watch?v=NgWujOrCZFo&list=PLkDaE6sCZn6GMoA0wbpJLi3t34Gd8l0aK

## Data Drift vs Concept Drift

### Data Drift (the "x" changes)

The input data distribution shifts compared to training data — the rules are the same, but the inputs look different.

**Example:** Speech recognition trained on studio-quality audio encounters real-world users speaking into cheap phone microphones in noisy environments. The language hasn't changed, but the audio quality (the input x) has drifted.

- Can be gradual (language evolves over years) or sudden (major environmental change)

### Concept Drift (the "x → y" mapping changes)

The relationship between inputs and correct outputs changes — the meaning of the data shifts.

**Example:** "That is sick!" meant "that person is ill" ten years ago; today it means "that is awesome." Same input (x), different correct output (y).

- **Gradual:** natural evolution of language or user behavior over time
- **Sudden shock:** overnight disruption (e.g., "Zoom" shifting from "go fast" to "video meeting" in 2020)

## Model Monitoring in Production

### Software Metrics

| Metric | Description |
|--------|-------------|
| **Latency (inference time)** | Milliseconds per prediction |
| **Throughput (FPS/QPS)** | Predictions processed per second |
| **GPU/compute usage** | Hardware utilization % |
| **Memory & server load** | System health |

### Input Metrics (Watch for Data Drift)

For a computer vision model:
- Average image brightness (lightbulb burned out?)
- Image blurriness/sharpness (camera bumped or dirty?)
- Resolution/image size (camera settings changed?)
- Color distribution (product line switched?)

### Output Metrics (Watch the AI's Behavior)

| Metric | What it signals |
|--------|----------------|
| **Average confidence score** | Drop from 95% → 40% means model is struggling |
| **Bounding boxes per image** | Sudden spike → model is hallucinating |
| **Null prediction (pass) rate** | 99% → 50% pass rate: something is wrong |
| **Human override rate** | How often humans correct the AI |

## Error Analysis and Prioritization

### HLP (Human Level Performance) Framework

Compare AI accuracy vs human accuracy by data slice, weighted by frequency:

```
Overall Impact = Gap to HLP × % of data
```

**Example for speech recognition:**

| Scenario | AI | Human | Gap | % Data | Impact |
|----------|-----|-------|-----|--------|--------|
| Clean speech | 94% | 95% | 1% | 60% | **0.6%** |
| People noise | 88% | 90% | 2% | 30% | **0.6%** |
| Car noise | 90% | 94% | 4% | 4% | 0.16% |
| Low bandwidth | 70% | 70% | 0% | 6% | **0%** |

**Key insight:** A 4% gap in a rare scenario contributes less than a 1% gap in a common scenario. Always weight by data frequency before prioritizing improvements.

## Deployment Strategies

### Canary Deployment

Named after the "canary in a coal mine" safety practice:
1. Deploy new model to a small fraction of traffic (e.g., 5%)
2. Monitor closely for errors, regressions, or anomalies
3. If healthy → gradually ramp up (10% → 20% → 100%)
4. If unhealthy → immediately roll back

**Why:** limits blast radius. If the new model is broken, only 5% of users are affected — not everyone.

### Blue-Green Deployment

Maintain two identical production environments:
- Blue = current live version
- Green = new version under test
- Switch traffic between them instantly; roll back by switching back

## Evaluation Metrics

### Confusion Matrix

For binary classification (positive = defect found):

| | Predicted Positive | Predicted Negative |
|---|---|---|
| **Actually Positive** | TP (True Positive) | FN (False Negative) |
| **Actually Negative** | FP (False Positive) | TN (True Negative) |

**Cheat code:** read backwards — second word (Positive/Negative) = what the AI predicted; first word (True/False) = was the AI right?

### Precision and Recall

**Precision** ("did we catch the right ones?"):
```
Precision = TP / (TP + FP)
```
Out of all positive predictions, how many were actually positive?

**Recall** ("did we catch them all?"):
```
Recall = TP / (TP + FN)
```
Out of all actual positives, how many did we correctly identify?

### Precision-Recall Tradeoff

You usually cannot maximize both simultaneously — tuning the model to be more sensitive (higher recall) also causes more false alarms (lower precision).

### Why Manufacturing Prefers High Recall

| Error type | Cost |
|------------|------|
| False Positive (flag clean phone) | Worker checks for 5 seconds → cheap |
| False Negative (ship defective phone) | Angry customer, returns, brand damage → expensive |

Manufacturing tolerates many false alarms (lower precision) to catch nearly every real defect (high recall). "Better safe than sorry."

### F1 Score

Harmonic mean of precision and recall — useful when you want a single balanced metric:
```
F1 = 2 · (Precision · Recall) / (Precision + Recall)
```

## Related Topics

- [[computer-vision]] — vision models deployed in production (defect detection, QA)
- [[object-detection]] — YOLO and other detectors monitored via these metrics
- [[neural-networks]] — the models being monitored
- [[probability-statistics]] — statistical foundations for evaluation metrics
