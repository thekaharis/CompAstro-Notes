---
type: concept
title: "Self-Supervised Learning"
created: 2026-04-14
updated: 2026-04-16
tags:
  - concept/ml
  - domain/inference
status: seed
complexity: intermediate
domain: "[[Inference and ML]]"
aliases:
  - "SSL"
  - "contrastive learning"
related:
  - "[[SKATR]]"
  - "[[Vision Transformer]]"
  - "[[Simulator Dependence]]"
  - "[[Cross-Simulator Generalization]]"
sources:
  - "[[Ore et al 2025 (SKATR)]]"
---

# Self-Supervised Learning

## Definition and Core Concept

Self-supervised learning (SSL) is a machine learning training paradigm where a model learns useful representations from **unlabeled data** by solving **pretext tasks** — auxiliary learning objectives designed to encourage the model to extract meaningful features without human annotation. The key insight is that the structure of the data itself provides a supervisory signal: if two different views of the same underlying data are related in a known way, a model can be trained to recognize that relationship without explicit labels.

In the context of 21cm cosmology and reionization, SSL offers a solution to a critical practical problem: generating labeled simulation data is expensive (each simulation takes hours to days), but generating unlabeled simulations is cheap (you just run the simulator without labeling outputs). SSL allows the model to learn from the cheap, abundant unlabeled data.

## Upstream (Pretext) vs. Downstream (Target) Tasks

A crucial distinction that drives the SSL workflow:

### Upstream Tasks (Pretext Tasks)

These are the self-supervised learning objectives solved **during pre-training** on large unlabeled datasets. The goal is not to solve these tasks per se, but to learn good **feature representations** as a byproduct. Examples include:

- **Contrastive learning**: Train the model so that two different augmentations of the same input produce similar embeddings ([[SimCLR]]), while different inputs produce dissimilar embeddings
- **Masked prediction**: Mask 75% of patches in an image and train the model to reconstruct the masked patches from the visible ones ([[MAE]])
- **Rotation prediction**: Rotate an image by a random multiple of 90° and train the model to predict the rotation angle
- **Temporal consistency**: For video data, train the model that successive frames should have similar embeddings

### Downstream Tasks (Target/Evaluation Tasks)

These are the tasks you actually care about, applied **after pre-training**:

- **Regression**: Predict cosmological parameters $(\Omega_m, \sigma_8, \tau, \ldots)$ from a 21cm field (target of [[SKATR]])
- **Classification**: Classify reionization morphology (inside-out vs. outside-in)
- **Simulation-based inference (SBI)**: Estimate posterior distributions $p(\theta | x_\text{obs})$ over cosmological parameters given observed 21cm data
- **Summary statistics extraction**: Compute large-scale features (power spectrum, correlation functions) from raw fields

### The Transfer Learning Process

The workflow is:

1. **Pre-train** the model backbone (e.g., a ViT) on a **large unlabeled dataset** (e.g., 10,000 21cm simulations from 21cmFAST) using a pretext task (e.g., contrastive learning)
2. **Freeze the backbone** weights
3. **Attach a small trainable head** (a few fully-connected layers) on top of the frozen backbone
4. **Fine-tune** the head on a **small labeled dataset** (e.g., 100 simulations where cosmological parameters are known)
5. **Evaluate** on held-out test data

The hypothesis is that the features learned during pre-training — which capture the intrinsic structure of 21cm fields — will be useful for downstream tasks. The small labeled dataset is sufficient because the hard work of feature learning is already done.

## Contrastive Learning: SimCLR and BYOL

### SimCLR Framework

SimCLR (Simple Contrastive Learning of Representations) is a widely-used SSL approach that works as follows:

1. **Data augmentation**: Take a single unlabeled sample $x$ (e.g., a 21cm lightcone) and create two different augmented views $x_i$ and $x_j$

2. **Encoder pass**: Pass both views through an encoder network (e.g., ViT) to get embeddings $z_i = \text{Encoder}(x_i)$ and $z_j = \text{Encoder}(x_j)$

3. **Projection head**: Project embeddings to a lower-dimensional space: $\tilde{z}_i = g(z_i)$ and $\tilde{z}_j = g(z_j)$ (where $g$ is an MLP, later discarded)

4. **Contrastive loss**: Train the model to maximize similarity between $\tilde{z}_i$ and $\tilde{z}_j$ while minimizing similarity to embeddings from other data points

The **InfoNCE (Noise Contrastive Estimation) loss** is:

$$L_{i,j} = -\log \frac{\exp(\text{sim}(\tilde{z}_i, \tilde{z}_j) / \tau)}{\sum_{k=1}^{2N} \exp(\text{sim}(\tilde{z}_i, \tilde{z}_k) / \tau)}$$

where:
- $\text{sim}(\mathbf{a}, \mathbf{b}) = \frac{\mathbf{a} \cdot \mathbf{b}}{|\mathbf{a}| |\mathbf{b}|}$ is **cosine similarity** between vectors
- $\tau$ is a temperature parameter (typically $\tau = 0.07$) that controls the "sharpness" of the softmax
  - Low $\tau$ makes the loss more selective (only very similar pairs count)
  - High $\tau$ makes the loss softer (more pairs contribute)
- The denominator is a sum over all $2N$ embeddings in the batch (both augmented views of both the data point itself and negative samples)

**Intuition**: The numerator is high when $\tilde{z}_i$ and $\tilde{z}_j$ (augmented views of the same data) are similar; the denominator is large when $\tilde{z}_i$ is similar to many things (both correct and incorrect partners). The loss drives the ratio up, encouraging the model to distinguish true pairs from false ones.

### Why Contrastive Learning Works

The hypothesis underlying contrastive learning is that:

> **Augmentation-invariant features are more physics-based and less simulator-specific.**

For 21cm data, the augmentations might be:
- Random rotations (rotating the spatial grid shouldn't change the underlying ionization physics)
- Redshift slices at different frequencies (different frequency channels sample slightly different redshift slices; the ionization field is continuous)
- Small noise additions (observational noise shouldn't destroy the physical signal)

A model trained to produce similar embeddings under these transformations is forced to learn features that capture the **robust, physics-based structure** of reionization (bubble topology, percolation behavior, scaling laws) and discard simulator-specific artifacts (grid noise, frequency resolution details).

### BYOL (Bootstrap Your Own Latent)

BYOL is an alternative contrastive approach that surprisingly works without negative samples:

1. Train an encoder network on pairs of augmented views $(x_i, x_j)$
2. Use $\mathbf{z}_i$ from one view to predict $\mathbf{z}_j^{(\text{slow})}$ from the other view, where the second network is a **slowly-updated copy** (an exponential moving average of the main network)
3. Minimize the difference between prediction and target

BYOL is simpler to implement (no need for large batches with negative samples) but still learns good representations. The key insight is that the slow-moving network acts as a form of regularization, preventing trivial solutions (e.g., collapse to a constant).

## Masked Autoencoder (MAE) Approach

### Concept

The Masked Autoencoder (MAE) framework, applied to images by He et al. (2021) and adapted to 21cm cosmology, works as follows:

1. **Masking**: Randomly mask 75% of the spatial patches in the input (for images) or 75% of the voxels (for 3D 21cm fields)

2. **Encoder**: Pass only the **visible patches** (25%) through an encoder network

3. **Decoder**: Use a decoder network to reconstruct the values of the **masked patches**

4. **Loss**: Compare reconstructed masked patch values to the ground truth and optimize the reconstruction error

The key parameters:
- **Masking ratio** (typically 0.75): How much of the input is hidden? A high ratio (75%) forces the model to infer large-scale structure from limited information, preventing the model from memorizing local patterns.
- **Encoder/decoder asymmetry**: The encoder processes only visible patches (cheap), while the decoder must reconstruct masked patches (expensive learning). This allows training large models efficiently.

### Why MAE Works Better Than Naive Masking

A naive approach might mask patches and require the model to predict them while seeing everything else. MAE is superior because:

1. **High masking ratio** (75%) removes almost all local information, forcing the model to learn **global structure** and long-range dependencies
2. **Information bottleneck**: The visible patches alone are insufficient to locally reconstruct masked regions; the model must integrate global context
3. **Scalability**: Because only 25% of patches are processed by the expensive encoder, training is ~4× faster than processing all patches

For 21cm data, the masked MAE approach forces the model to learn:
- Global bubble topology (from local patches, infer large-scale ionization structure)
- Percolation patterns (how ionized regions connect)
- Power-law scaling (how small-scale fluctuations relate to large-scale structure)

## Why Self-Supervised Representations Generalize Better

A central claim in [[SKATR]] and related work is that **self-supervised pre-training improves cross-simulator generalization**. The hypothesis:

### Simulator-Specific vs. Physics-Based Features

**Supervised learning** on a single simulator (e.g., 21cmFAST) learns features that are a mixture of:
- **Physics-based features**: The true reionization physics (bubble growth, ionization balance)
- **Simulator artifacts**: Numerical aspects of 21cmFAST (discretization, approximation choices, excursion-set assumptions)

A supervised model trained entirely on 21cmFAST will over-fit to simulator artifacts and perform poorly when applied to a different simulator (e.g., SCRIPT) or to real observations.

**Self-supervised learning** on unlabeled data from the simulator learns representations via augmentation-invariance:
- Features that change under physical transformations (rotations, redshift slices) are suppressed
- Features that are invariant under augmentations are encouraged
- Simulator artifacts are often **not** invariant under augmentations (e.g., grid artifacts change under rotation), so they are naturally suppressed

After pre-training, a small amount of labeled data from one simulator fine-tunes the model for that simulator, but the underlying representations remain more universal.

### Testing the Hypothesis

Testing whether self-supervised representations are truly more physics-based is a key research question that SKATR addresses:

1. Pre-train on unlabeled 21cmFAST data using contrastive learning
2. Fine-tune on labeled 21cmFAST data; evaluate on held-out 21cmFAST test set (in-distribution)
3. Fine-tune on labeled 21cmFAST data; evaluate on SCRIPT test set at different resolution (cross-simulator)
4. Compare to a supervised baseline trained entirely on labeled 21cmFAST data

If self-supervised pre-training improves cross-simulator generalization (step 3), it suggests the learned representations are more physics-based. SKATR reports that this is indeed the case.

## Specific Augmentations for 21cm Data

The choice of augmentations is crucial for SSL; augmentations should preserve **physical meaning** while breaking **simulator artifacts**. For 21cm lightcone simulations:

### Spatial Transformations

- **Random rotations** (in-plane rotations by 90°, 180°, 270°): Ionization physics is isotropic; rotating the spatial grid shouldn't change bubble statistics
- **Random flips** (mirror along x, y axes): Reionization morphology has no preferred handedness

### Frequency/Redshift Slices

- **Extracting different redshift slices**: A 3D lightcone $(x, y, \nu)$ can be sliced along the frequency axis at different $\nu$ values, sampling slightly different redshifts. The ionization field varies smoothly with redshift, so different slices are related.
- **Frequency averaging**: Smooth the data slightly across frequencies to account for the fact that the frequency resolution is arbitrary

### Noise Additions

- **Gaussian noise**: Add small random Gaussian noise to account for observational/thermal noise in real 21cm observations. The underlying ionization physics should be robust to small noise.
- **Poisson noise** (for counts-based data): Add noise consistent with photon statistics if the data represents photon counts

### Physics-Preserving Augmentations

- **Avoid augmentations that break physics**:
  - Don't randomly stretch or rescale spatial axes (this changes the physical scale of bubbles)
  - Don't apply arbitrary phase shifts (this breaks correlations)
  - Don't mask large contiguous regions (this removes too much information to be useful)

## Two-Stage Transfer Learning in Detail

The full workflow for SSL in 21cm inference:

### Stage 1: Pre-training on Large Unlabeled Dataset

- **Data**: 10,000–100,000 unlabeled 21cm simulations from 21cmFAST, spanning a grid of cosmological parameters
- **Method**: SimCLR or MAE with the augmentations listed above
- **Objective**: Maximize the contrastive loss (SimCLR) or minimize reconstruction error (MAE) on the unlabeled data
- **Result**: A pre-trained backbone network (e.g., ViT-Base) with learned feature extraction capabilities
- **Computational cost**: ~10 GPU-days (the one-time cost; amortized over all downstream tasks)

### Stage 2: Fine-tuning on Small Labeled Dataset

- **Data**: 100–1,000 labeled simulations where cosmological parameters are known (e.g., $\Omega_m, \sigma_8, \tau, \ldots$)
- **Method**: Freeze the pre-trained backbone; attach a small trainable head (2–3 fully-connected layers)
- **Objective**: Minimize regression loss on the downstream task (e.g., predict $\theta_i$ from field)
- **Result**: A task-specific model that maps 21cm fields to cosmological parameters
- **Computational cost**: ~1–10 GPU-hours

### Why This Beats Pure Supervised Learning

Consider the alternative:
- **Pure supervised**: Train a model from scratch on 1,000 labeled simulations
- **SSL + fine-tune**: Pre-train on 10,000 unlabeled, then fine-tune on 100 labeled

SSL wins because:
1. The pre-trained model learns general structure from 10,000 samples
2. The fine-tuning step is cheap and focused: it only adapts the model to the specific task and cosmological parameter space
3. Generalization is better because the backbone wasn't over-fit to the limited labeled dataset

**Quantitative comparison**: In computer vision, SSL pre-training typically gives a 10–20% improvement in accuracy on downstream tasks with limited labeled data (~100–1000 samples). On 21cm data, the gains can be even larger because unlabeled simulations are particularly cheap.

## Comparison to Purely Supervised Learning

### When Supervised Learning Is Competitive

If sufficient labeled data is available (e.g., 1,000 labeled simulations from a single simulator), supervised learning with an appropriate architecture (large ViT) can match or beat SSL in **in-distribution performance** (evaluation on the same simulator). This is because:

1. The supervised model directly optimizes the objective (no auxiliary pretext task)
2. With enough labeled examples, the model has enough capacity and data to learn good features without pre-training

### When SSL Is Superior

SSL's advantages grow as labeled data becomes scarce:

- **100 labeled samples**: SSL pre-training typically gives 10–20% improvement in downstream task accuracy
- **1,000 labeled samples**: SSL advantage diminishes to 5–10%
- **10,000 labeled samples**: SSL and supervised learning converge to similar performance

Additionally, **SSL generalizes better cross-simulator**: a supervised model trained on 21cmFAST performs poorly on SCRIPT, while an SSL-pretrained model transfers better.

## Why 21cm Data Specifically Benefits from SSL

The 21cm field is particularly amenable to SSL for several reasons:

### 1. Expensive Labeling

Each 21cm simulation:
- Takes 10 minutes–10 hours to compute (depending on resolution and code)
- Produces a high-dimensional output (e.g., a $256^3$ brightness temperature field)
- Requires manual annotation to extract meaningful labels (cosmological parameters, morphology classification)

Unlabeled simulations are cheap: once the code is running, you can generate thousands of independent realizations by just varying random seeds.

### 2. Large Unlabeled Dataset Easily Available

The community has access to or can generate:
- Thousands of 21cmFAST simulations across cosmological parameter space (the [[Training Set Generation]])
- Open-source codes that can generate simulations rapidly
- Diverse simulators (SCRIPT, ASTRID, etc.) providing multiple views of the same underlying physics

### 3. Robust Physical Structure

21cm fields have strong, characteristic physical structure:
- Bubble topology is consistent across diverse simulation scenarios
- The percolation transition occurs around the same redshift for similar cosmological parameters
- Scaling laws (bubble size distribution, power spectrum slope) are robust

This robustness suggests that physics-based representations learned via SSL will be more useful than simulator-specific artifacts learned via supervised learning.

### 4. Simulator Dependence Problem

As discussed in [[Simulator Dependence]], different simulators (21cmFAST, SCRIPT, ASTRID) produce somewhat different predictions for the same cosmological parameters. SSL offers a direct solution: by learning representations invariant under augmentations, the model implicitly learns features that are common across simulators, reducing dependence on any particular code's artifacts.

## Connections to This Thesis

Self-supervised learning appears in this thesis in two places:

1. **[[SKATR]]**: A specific SSL application to 21cm cosmology, using contrastive pre-training + ViT architecture for downstream regression of cosmological parameters. SKATR demonstrates that SSL pre-training improves both in-distribution accuracy and cross-simulator generalization.

2. **[[Cross-Simulator Generalization]]**: SSL is one strategy for addressing the [[Simulator Dependence]] problem — by learning representations that are invariant under domain-relevant augmentations, the model naturally becomes less dependent on the specific simulator used for training.

3. **Comparison to [[EFT Approach]]**: Both SSL and EFT address simulator dependence, but from different angles:
   - **EFT**: Decomposes the physics into simulator-independent (universal) and simulator-dependent (EFT coefficients) pieces; coefficients are tuned to match observations
   - **SSL**: Learns representations that are augmentation-invariant, implicitly suppressing simulator artifacts; representations are tuned on downstream tasks

The two approaches are complementary and can be combined: one could train an SSL model on semi-numerical simulation outputs, use the learned representations as input to an EFT inference pipeline, and then calibrate EFT coefficients. This hybrid approach is not explored in the current thesis but represents a promising future direction.
