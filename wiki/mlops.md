# MLOps (Machine Learning Engineering for Production)

MLOps (Machine Learning Operations) is an emerging discipline comprising the tools and principles to support progress through the ML project lifecycle. A model that performs well in the lab can degrade silently in the real world — MLOps provides the discipline to detect and respond to that.

## Source

- `raw/04-machine-learning-engineering-for-production-mlops/Machine Learning Engineering for Production (MLOps).md`
- Course: https://www.youtube.com/watch?v=NgWujOrCZFo&list=PLkDaE6sCZn6GMoA0wbpJLi3t34Gd8l0aK

## ML Project Lifecycle

Every ML project flows through four stages, with strong feedback loops — later stages frequently push work back to earlier ones:

```
Scoping → Data → Modeling → Deployment
```

| Stage | Steps | Key questions |
|---|---|---|
| **Scoping** | Define project | What problem? What metrics? What's feasible? |
| **Data** | Define data and establish baseline; Label and organize data | Is the data consistent? Are labels ambiguous? How to handle edge cases? |
| **Modeling** | Select and train model; Perform error analysis | Model-centric or data-centric? Where does HLP gap exist? |
| **Deployment** | Deploy in production; Monitor and maintain system | Concept drift? Data drift? Uptime? Integration? |

**Key insight:** ML model code (X→Y) is only **5–10% of the total code** in a production ML system. The rest is infrastructure: data pipelines, monitoring, serving, config management.

In research, focus is on generalization: can the system handle more scenarios? In a commercial context, the questions are more concrete: Does it work? Does it keep working? What is the throughput? What is the uptime? Does it integrate into an existing workflow? Does it save money?

### First Deployment vs. Maintenance

First deployment is a one-time push through all four stages. Maintenance is ongoing — deployed models face two forces that pull them back upstream:
- **Software issues** → push work back to the Deployment stage
- **Concept drift / data drift** → push work all the way back to Data or Modeling

Maintenance is almost always harder than first deployment.

## Data: Structured vs. Unstructured

| Type | Examples |
|---|---|
| **Unstructured** | Images, audio, text (HLP — humans label these naturally) |
| **Structured** | Tabular data: user IDs + purchase history, product IDs + inventory counts |

Unstructured data benefits most from deep learning. Structured data often works well with traditional ML.

### Model-Centric vs. Data-Centric AI

The Modeling stage has two schools of thought:

- **Model-centric:** fix the dataset; iterate on the model architecture and hyperparameters
- **Data-centric:** fix the model architecture; iterate on the dataset quality and consistency

In practice, most improvements in production come from data quality improvements, not model changes. Data-centric AI is increasingly the right default for applied work.

### Rare Classes and Skewed Distributions

When data is heavily skewed (e.g., 99% negative, 1% positive), a model that always predicts "negative" achieves 99% accuracy — and is completely useless. This is the **rare class problem**.

Example from medical imaging — ChexXNet (121-layer CNN) for chest X-ray classification:

| Condition | Training samples | Accuracy |
|---|---|---|
| Effusion | ~10,000 | 0.901 |
| Edema | ~10,000 | 0.924 |
| Mass | ~10,000 | 0.909 |
| Hernia | ~100 | 0.851 |

Hernia has only ~100 training samples — performance is lower and reliability is uncertain despite a 0.851 accuracy number.

### Establishing a Baseline

Before training models, establish **Human Level Performance (HLP)** as a baseline. HLP tells you:
- Where there is room to improve (gap between AI and HLP)
- Where the ceiling is (when HLP = 100%, there is a theoretical upper bound)

For unstructured data (images, audio), humans perform well and HLP is informative. For structured data, HLP is less useful.

### Data Consistency: The Speech Recognition Example

For speech recognition, key data quality questions:
- Are loud and quiet parts of audio clips normalized? (consistency)
- How to handle silence at start/end of clips? (normalization)
- Are rude or offensive mis-transcriptions handled? (safety)
- Is labeling consistent across annotators? (inter-annotator agreement)

### Sanity Check Before Full Training

Always overfit a tiny training dataset first:
- Speech recognition: a few audio/transcript pairs (x → y)
- Image segmentation: 1–5 images with masks
- Image classification: 10–50 images per class

If the model can't overfit 5 examples, there is a bug in the code before you waste compute on the full dataset.


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

**Prioritization example for speech recognition:**

| Scenario | AI Accuracy | HLP | Gap to HLP | % of Data | Weighted Impact |
|---|---|---|---|---|---|
| Clean speech | 94% | 95% | 1% | 60% | **0.6%** |
| People noise | 87% | 89% | 2% | 30% | **0.6%** |
| Car noise | 89% | 93% | 4% | 4% | 0.16% |
| Low bandwidth | 70% | 70% | 0% | 6% | **0%** |

**Key insight:** the 4% car noise gap sounds critical, but it only contributes 0.16% overall impact because it represents just 4% of real traffic. Clean speech (60% of traffic) and people noise (30% of traffic) both deserve attention first despite smaller gaps. Always weight by data frequency before prioritizing.

### Error Analysis Checklist

When a model underperforms on a data slice, brainstorm:
- Accuracy on different demographic groups (genders, ethnicities, accents)
- Accuracy on different devices or sensor configurations
- Prevalence of mis-predictions that could cause harm (rude mis-transcriptions, offensive outputs)

Then establish metrics to assess performance against each issue on appropriately-sized slices of held-out data.

### Multi-Class Metrics

For multi-class problems (manufacturing defects: Scratch, Dent, Pit mark, Discoloration), track per-class precision, recall, and F1:

| Defect Type | Precision | Recall | F1 |
|---|---|---|---|
| Scratch | 82.1% | 99.2% | 89.8% |
| Dent | 92.1% | 99.5% | 95.7% |
| Pit mark | 85.3% | 98.7% | 91.5% |
| Discoloration | 72.1% | 97% | 82.7% |

Discoloration has the weakest precision (72.1%) — the model catches nearly all discolored parts (97% recall) but generates many false alarms. This drives prioritization: improving discoloration precision is the clearest next step.

## Deployment Strategies

### Shadow Mode

Before fully deploying a new model, run it in **shadow mode**:
- The ML system runs in parallel alongside the existing system (human or prior model)
- The ML system's output is **not used for any decisions** during this phase
- Both the human decision and the ML prediction are logged

**Visual inspection example:** three phones pass through a quality check — one clean, one scratched (human catches it, ML misses), one scratched (human misses it, ML catches it). Shadow mode reveals these divergences safely before anyone acts on the ML output. You audit the disagreements to understand where the model fails before you trust it.

Shadow mode is the safest way to validate a new model in production conditions without risk.

### Canary Deployment

Named after the "canary in a coal mine" safety practice:
1. Deploy new model to a small fraction of traffic (e.g., 5%)
2. Monitor closely for errors, regressions, or anomalies
3. If healthy → gradually ramp up (10% → 20% → 100%)
4. If unhealthy → immediately roll back

**Why:** limits blast radius. If the new model is broken, only 5% of users are affected — not everyone.

### Blue-Green Deployment

Maintain two identical production environments:
- Blue = current live (old) version
- Green = new version under test
- A router splits traffic between them; switch 100% to green when ready; roll back instantly by switching traffic back to blue

The key advantage is zero-downtime rollback — you never have to "undeploy" anything, just redirect the router.

## Evaluation Metrics

### Confusion Matrix

For binary classification (positive = defect found):

| | Predicted Positive (y=1) | Predicted Negative (y=0) |
|---|---|---|
| **Actually Positive (y=1)** | TP (True Positive) | FN (False Negative) |
| **Actually Negative (y=0)** | FP (False Positive) | TN (True Negative) |

**Cheat code:** read backwards — second word (Positive/Negative) = what the AI predicted; first word (True/False) = was the AI right?

**Concrete example** — phone defect detection over 1,000 inspections:

| | Predicted Positive | Predicted Negative |
|---|---|---|
| **Actually Positive** | 68 (TP) | 18 (FN) |
| **Actually Negative** | 9 (FP) | 905 (TN) |

From these numbers:
```
Precision = 68 / (68 + 9)  = 68 / 77  ≈ 88.3%
Recall    = 68 / (68 + 18) = 68 / 86  ≈ 79.1%
```

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
