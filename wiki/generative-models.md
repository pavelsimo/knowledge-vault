# Generative Models

Generative models learn the probability distribution of data, enabling them to synthesize new samples. Unlike discriminative models (which learn P(y|x)), generative models learn P(x) or P(x|y). This topic covers the full taxonomy: autoencoders, VAEs, GANs, and diffusion models.

## Source

- `raw/03-stanford-cs231n/Stanford CS231N.md`

## Discriminative vs Generative

| Model type | Learns | Question |
|-----------|--------|----------|
| **Discriminative** | P(y\|x) | "Given this image, what's the probability it's a cat?" |
| **Generative** | P(x) | "What kinds of images exist, and how likely are they?" |
| **Conditional generative** | P(x\|y) | "Generate an image, given that the label is cat." |

**When to use generative models:** whenever there is ambiguity in the output. Asking for "a dog wearing a hot-dog hat" has many valid answers — generative models capture this distribution.

## Taxonomy of Generative Models

From Goodfellow's "Tutorial on Generative Adversarial Networks" (adapted in CS231N):

```
Generative Models
├── Can compute P(x) directly
│   ├── Explicit Density
│   │   ├── Tractable density → Autoregressive models (PixelCNN, GPT)
│   │   └── Approximate density → Variational Autoencoder (VAE) — optimize ELBO
│   └── Iterative procedure to approximate samples → (see implicit)
└── Cannot compute P(x), but can sample from P(x)
    └── Implicit Density
        ├── Direct sampling → Generative Adversarial Network (GAN)
        └── Indirect (iterative) → Diffusion Models
```

The key split: **explicit** models reason about probabilities directly, **implicit** models just generate samples without assigning likelihoods.

## Training Objective: Maximum Likelihood

All generative models optimize maximum likelihood:
```
W* = argmax_W Σᵢ log p(x⁽ⁱ⁾; W)
```
- Log trick converts product over examples into a sum (avoids underflow, easier optimization)
- Equivalent to minimizing **Negative Log Likelihood (NLL)**

## Autoencoders

An autoencoder compresses input x into a latent code z, then reconstructs x from z:

```
Input x → Encoder → z (latent/bottleneck) → Decoder → Reconstructed x
```

- The bottleneck forces the model to learn efficient compression
- Encoder: MLP, CNN, or Transformer depending on task
- Decoder: learns to "draw" from latent representation
- Training: minimize reconstruction loss (L2 or perceptual loss)

**Where "auto" comes from:** the label is automatically the input itself — no human annotation.

Key papers:
- [Reducing the Dimensionality of Data with Neural Networks (Hinton & Salakhutdinov)](https://www.cs.toronto.edu/~hinton/absps/science.pdf)

## Variational Autoencoders (VAEs)

VAEs extend autoencoders to be **probabilistic generative models**. Instead of encoding x to a fixed z, the encoder outputs a distribution q(z|x) (mean and variance).

**VAE generative process:**
1. Sample z from prior `p(z)` (e.g., Gaussian)
2. Sample x from conditional `p_θ(x | z)` using the decoder

After training, generate new data: `sample z from p(z) → feed to decoder → get new x`. The latent z encodes factors like object identity, appearance, orientation, scene type.

**Problem:** computing the true posterior P(z|x) is **intractable** (the integral over all possible z is too hard).

**Solution — ELBO derivation:**
```
log p_θ(x) = log [p_θ(x|z)p(z)] / p_θ(z|x)
           = log [p_θ(x|z)p(z)q_φ(z|x)] / [p_θ(z|x)q_φ(z|x)]
```
Applying Jensen's inequality to lower-bound the log-likelihood:
```
ELBO = E[log P(x|z)] - KL(q(z|x) || p(z))
```
- Reconstruction term: decoder should reconstruct x from z
- KL term: keep the learned distribution close to the prior (usually Gaussian)

**Comparison of three generative model training objectives:**
```
Autoregressive: p_θ(x) = Π p_θ(xᵢ | x₁,...,xᵢ₋₁)   ← directly maximize likelihood

VAE:            p_θ(x) = ∫ p_θ(x|z)p(z)dz ≥ E[log p_θ(x|z)] - D_KL(q_φ(z|x) || p(z))
                          ← maximize ELBO (lower bound on likelihood)

GAN:            give up modeling p(x), but draw samples from p(x)   ← adversarial training
```

**Analogy:** you can't reach the cloud (true density) with your ruler, but you can push a floor (ELBO) up toward it as high as possible.

**Applications:** face generation, audio synthesis, molecule design, interpolation between styles.

Papers:
- [Auto-Encoding Variational Bayes (Kingma & Welling)](https://arxiv.org/pdf/1312.6114)

## Autoregressive Models

Model P(x) as a product of conditional probabilities:
```
p(x) = Π p(xₜ | x₁, ..., xₜ₋₁)
```

- GPT/LLMs are autoregressive models: predict the next token given all previous tokens
- Training: masked self-attention ensures no peeking at future tokens
- PixelCNN applies this to images (predict each pixel given all previous pixels)

Limitation: images are 2D and continuous — breaking them into a 1D sequence is awkward.

Papers:
- [Pixel Recurrent Neural Networks](https://arxiv.org/pdf/1601.06759)
- [Conditional Image Generation with PixelCNN Decoders](https://arxiv.org/pdf/1606.05328)

## GANs (Generative Adversarial Networks)

Two networks compete in a **minimax game**:
- **Generator G:** takes random noise z → produces fake image G(z)
- **Discriminator D:** tries to distinguish real images x from fakes G(z)

**Goal:** the generator learns to fool the discriminator until D can no longer distinguish fake from real. At equilibrium: p_G = p_data.

**Analogy:** forger (G) vs. detective (D). Forger improves to create more convincing fakes; detective improves to catch them.

**Training challenges:**
- No stable loss curve to monitor progress
- Unstable training (mode collapse, oscillation)
- Hard to scale to large models

**Timeline:** GANs dominated generative image modeling from 2016–2021 before diffusion models took over.

Papers:
- [Generative Adversarial Nets (Goodfellow et al., 2014)](https://arxiv.org/pdf/1406.2661)
- [Unsupervised Representation Learning with Deep Convolutional GANs (DCGAN)](https://arxiv.org/pdf/1511.06434) — first GAN to work on non-toy data
- [A Style-Based Generator Architecture for GANs (StyleGAN)](https://arxiv.org/pdf/1812.04948)

## Diffusion Models

Diffusion models generate images by **iteratively denoising** random noise:

**Forward process (training):** gradually add Gaussian noise to a real image over T steps until it becomes pure noise.

**Reverse process (inference):** a neural network learns to predict and remove the noise step-by-step, starting from pure noise.

**Why they work:** by learning to denoise slightly noisy images, the network implicitly learns the data distribution.

Papers:
- [Denoising Diffusion Probabilistic Models (DDPM)](https://arxiv.org/pdf/2006.11239)
- [Score-Based Generative Modeling through Stochastic Differential Equations](https://arxiv.org/pdf/2011.13456)

### Rectified Flow

Rectified flow trains the model to move along **straight paths** from noise to data (instead of the curved paths of DDPM):
- Faster inference (fewer steps needed — sometimes just 1-4)
- Simpler training objective (v-prediction: predict the "velocity" from noise to data)
- Used in Stable Diffusion 3, FLUX

Paper: [Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow](https://arxiv.org/pdf/2209.03003)

### Classifier-Free Guidance (CFG)

Standard conditional generation used a separate classifier to steer toward a text prompt — complex and noisy. CFG trains one model that handles both:
- 50% of the time: sees the condition (text, label) → learns p(x|y)
- 50% of the time: condition replaced with null → learns p(x)

At inference, combine both:
```
score = score_unconditional + w × (score_conditional - score_unconditional)
```
Higher guidance weight w → samples more strongly matching the condition.

Paper: [Classifier-Free Diffusion Guidance](https://arxiv.org/pdf/2207.12598)

### Latent Diffusion Models (LDMs)

Running diffusion in pixel space is expensive. LDMs compress images into a lower-dimensional latent space first:
1. Train a VAE to compress images into latent codes
2. Run the diffusion process in this compact latent space
3. Decode the final latent back to pixels with the VAE decoder

**LDM architecture (from Rombach et al., "High-Resolution Image Synthesis with Latent Diffusion Models", CVPR 2022):**
- Left side: VAE with Encoder (Image H×W×3 → Latent H/D × W/D × C) + Decoder + Discriminator (GAN loss)
- Center: Diffusion model trained to remove noise from **latents** (encoder is frozen during diffusion training)
- Right side at inference: sample random latent → iteratively apply diffusion model to denoise → run decoder → final image

Modern LDM pipelines use **VAE + GAN + Diffusion** — each component handles what it's best at.

State of the art: VAE + GAN (for the encoder/decoder) + Diffusion (for the generation process).

Paper: [High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/pdf/2112.10752)

### Diffusion Transformer (DiT)

Replace the U-Net backbone inside diffusion models with a Transformer:
- Scales better with compute than U-Net
- Used in Stable Diffusion 3, FLUX, Sora

Paper: [Scalable Diffusion Models with Transformers](https://arxiv.org/pdf/2212.09748)

### Text-to-Image and Text-to-Video

- **Text-to-image:** FLUX (Black Forest Labs), Stable Diffusion 3
- **Text-to-video:** Sora (OpenAI), MovieGen (Meta), HunyuanVideo (Tencent), Wan (Alibaba), Cosmos (NVIDIA)

Papers:
- [Photorealistic Video Generation with Diffusion Models (Sora)](https://arxiv.org/pdf/2312.06662)
- [HunyuanVideo](https://arxiv.org/pdf/2412.03603)
- [Cosmos World Foundation Model Platform for Physical AI](https://arxiv.org/pdf/2501.03575)

### Diffusion Distillation

Diffusion models are slow at inference (many denoising steps). Distillation techniques compress them to fewer steps:
- [Progressive Distillation for Fast Sampling of Diffusion Models](https://arxiv.org/pdf/2202.00512)
- [Consistency Models](https://arxiv.org/pdf/2303.01469)
- [Adversarial Diffusion Distillation (ADD)](https://static1.squarespace.com/static/6213c340453c3f502425776e/t/65663480a92fba51d0e1023f/1701197769659/adversarial_diffusion_distillation.pdf)

## Current State (2025)

- GANs: historically important, mostly replaced
- Diffusion models: dominant for image and video generation
- Autoregressive models: dominant for language; increasingly used for images
- Reference article: [Perspectives on diffusion (Sander Dieleman)](https://sander.ai/2023/07/20/perspectives.html)

## Related Topics

- [[self-supervised-learning]] — MAE and contrastive learning are related unsupervised methods
- [[attention-transformers]] — DiT uses transformers; VAEs use attention in modern variants
- [[neural-networks]] — backprop, loss functions underlying all generative models
- [[robot-learning]] — diffusion policy applies diffusion to robot action generation
- [[3d-vision]] — NeRF and Gaussian Splatting as specialized generative/representation models
