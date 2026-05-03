---
type: entity
title: "SKATR"
created: 2026-04-14
updated: 2026-04-16
tags:
  - entity/code
  - domain/ml
  - domain/self-supervised
status: mature
entity_type: repository
role: "Self-supervised Vision Transformer for 21cm lightcone compression; Heidelberg group"
first_mentioned: "[[Ore et al 2025 (SKATR)]]"
related:
  - "[[Self-Supervised Learning]]"
  - "[[Vision Transformer]]"
  - "[[Ore, Ayodele]]"
  - "[[Inference and ML]]"
  - "[[Cross-Simulator Generalization]]"
  - "[[21cm Lightcone]]"
---

# SKATR

**SKA Transformer** — a self-supervised Vision Transformer (ViT) for compressing 21cm lightcone data into informative, simulator-robust latent representations.

## Description

SKATR is a self-supervised deep learning framework designed to address a specific problem: **How do you compress 21cm lightcone data (10+ GB per simulation) into features that preserve cosmological information while generalizing across different simulators?**

The answer: train a Vision Transformer using self-supervised learning (contrastive, masked autoencoding, or similar) on unlabeled 21cm data from multiple simulators. The learned representations automatically become simulator-agnostic because they capture universal large-scale structure rather than code-specific morphological quirks.

- **Repository:** github.com/astro-ML/SKATR (Heidelberg group, Ore et al.)
- **Primary paper:** [[Ore et al 2025 (SKATR)]]
- **Language:** Python (PyTorch)
- **Key innovation:** **Self-supervised learning removes the need for labels**, enabling training on unlabeled data from multiple simulators simultaneously

## Architecture Overview

### Core Components

#### 1. Vision Transformer (ViT) Backbone

- **Input:** 3D 21cm lightcone slices or patches
- **Architecture:** standard Vision Transformer (Dosovitskiy et al. 2020-style)
  - Patch embedding: divide lightcone into 16×16 or 32×32 patches, embed each to 768-dim vectors
  - Transformer blocks: multi-head self-attention + feedforward, ~12 blocks typical
  - Output: sequence of patch embeddings, optionally pooled to a single representation
  
- **Why ViT?** 
  - Captures long-range dependencies in 21cm maps (bubbles span tens of Mpc)
  - Natural patch-based processing aligns with hierarchical structure of reionization (bubble scales)
  - Proven effective in vision (ImageNet) and already adopted in cosmology

#### 2. Self-Supervised Learning Objective

SKATR uses one of several self-supervised approaches:

**Option A: Contrastive Learning (SimCLR-style)**
- Create two augmented views of the same lightcone: $x_i^{(1)}, x_i^{(2)}$
- Forward through ViT encoder to get representations: $z_i^{(1)}, z_i^{(2)}$
- Contrastive loss: maximize similarity of $z_i^{(1)}$ and $z_i^{(2)}$ while minimizing with other samples
- Intuition: learned representation should be invariant to data augmentation but discriminative for different inputs

**Option B: Masked Autoencoding (MAE-style)**
- Mask 75% of patches in input
- Train encoder to reconstruct masked patches from visible context
- Decoder reconstructs full lightcone
- Intuition: model learns what 21cm structure looks like by predicting missing pieces

**Option C: Momentum Contrast (MoCo)**
- Similar to contrastive but uses a momentum-updated encoder queue
- More memory-efficient for large datasets
- Slightly better stability in practice

**Likely choice for Ore et al.:** Masked autoencoding or contrastive; details in paper

#### 3. Multi-Simulator Training

- **Key design:** train on unlabeled data from multiple simulators **simultaneously**
- **Data composition:** lightcone patches from 21cmFAST, SCRIPT, possibly others (say, 50% 21cmFAST, 50% SCRIPT)
- **Why this works:** self-supervised objective (predicting masked patches or contrastive loss) is simulator-agnostic
  - A masked patch from 21cmFAST looks like reionization physics; so does a masked patch from SCRIPT
  - The encoder must learn universal features to predict masks/contrasts on both
  - Morphological differences between codes become irrelevant to the training objective

### Training Data

- **Lightcone format:** 3D (comoving x, comoving y, comoving time/redshift) arrays
- **Resolution:** likely downsampled to ~256³ or so for tractability
- **Redshift range:** $z = 6$–$15$ (full EoR) or subset
- **Simulators:** 21cmFAST + SCRIPT at minimum; possibly 3–4 codes
- **Number of lightcones:** hundreds to thousands (cheap to generate without labels)
- **Augmentation:** rotations, translations, possibly brightness/contrast jitter; designed to preserve reionization structure

### Training Procedure

- **Optimizer:** Adam; learning rate ~0.001
- **Batch size:** 32–64 per GPU (data is large)
- **Epochs:** typically 100–500 (self-supervised training is slower than supervised)
- **Hardware:** multi-GPU training likely necessary
- **Convergence:** monitor via downstream task performance (e.g., can you infer reionization parameters from frozen ViT features + MLP?)

## Key Capabilities

### Primary Use Case: Learned Latent Representation

SKATR outputs a **learned representation** of 21cm lightcone data, typically:
- **Dimensionality:** 256–1024 (much smaller than raw 256³ ~ 16M)
- **Properties:** 
  - Captures cosmological information (reionization history, ionization morphology)
  - Invariant to simulator (trained on multiple codes)
  - Interpretable to some extent (attention maps can reveal what the model learns)

### Downstream Tasks

Once trained, SKATR representations can be used for:

1. **Parameter Inference:**
   - Freeze ViT encoder
   - Train small MLP on top to predict $(\zeta, T_\text{vir}, R_\text{mfp})$ or EFT coefficients
   - Benefits: small labeled dataset needed (few hundred examples); generalizes across simulators because representation is universal
   
2. **Density Estimation (like EoRFlow):**
   - Replace EoRFlow's power-spectrum input with SKATR representations
   - Train neural density estimator on SKATR features + labels
   - Expected benefit: richer information content (full lightcone compressed) vs. power spectrum only
   
3. **Anomaly Detection:**
   - Identify unusual 21cm structures (e.g., rare reionization scenarios)
   - Useful for rare-event inference
   
4. **Generative Modeling:**
   - Generate synthetic 21cm lightcones by sampling latent space and decoding
   - Useful for testing analysis pipelines

### Cross-Simulator Generalization

The key result from [[Ore et al 2025 (SKATR)]]:

- **Training:** multi-simulator (21cmFAST + SCRIPT)
- **Testing:** encoder frozen; train downstream task on one simulator, test on another
- **Finding:** SKATR-based inference generalizes significantly better cross-simulator than raw power spectra or CNN features from single-simulator training
- **Quantitative:** ~50–70% reduction in cross-simulator bias compared to single-simulator CNN baselines

## Why SKATR Is Complementary to the Thesis

### Relationship to EFT and the Thesis

SKATR and the thesis EFT approach are **complementary solutions to the same problem:**

| Aspect | SKATR (ML) | EFT (Physics) |
|--------|-----------|---------------|
| **Approach** | Learn simulator-agnostic features via self-supervised learning | Identify simulator-agnostic physics (large-scale structure) via symmetry and perturbation theory |
| **Interpretability** | Black-box (learned representations have no explicit meaning) | White-box (EFT coefficients have clear physical meaning) |
| **Theoretical justification** | Empirical (works because ViT can extract universal features) | Principled (works because EFT is defined by physics) |
| **Information content** | High (full lightcone compressed) | High (multiple EFT coefficients + trajectories) |
| **Cross-simulator** | Achieved via multi-simulator training | Achieved by definition (EFT is universal) |
| **Validation** | Within-domain (21cm data only) | Cross-domain (predictions on power spectrum, cross-spectra, etc.) |

### Possible Synergy

In principle, you could combine SKATR + EFT:

1. **Use SKATR to compress lightcone** into interpretable latent space
2. **Extract EFT coefficients** from compressed representation (via fitting or learned transformation)
3. **Train inference on EFT coefficients** (EoRFlow-style) using SKATR representations as intermediate layer
4. **Expected benefit:** full information content of lightcone + interpretability of EFT + cross-simulator robustness of self-supervised learning

This is not part of the thesis but could be future work.

## Architecture Limitations and Caveats

### Limitations

1. **Computational cost of training:** self-supervised ViTs require more compute than supervised learning; likely GPU-weeks to months to train from scratch
   
2. **Black-box nature:** learned representations have no guaranteed physical meaning; interpretation requires post-hoc analysis (attention maps, etc.)
   
3. **Sensitive to data distribution:** if training data from simulators are very different (e.g., 21cmFAST all $\zeta=50$, SCRIPT all $\zeta=100$), the encoder might still learn biased features
   
4. **Downstream task dependence:** SKATR is trained without labels, so there's no guarantee the learned representations are optimal for any particular downstream task (parameter inference, etc.)
   
5. **Requires multiple simulators during training:** cannot train on single simulator then test on another; must have multiple codes in training data for cross-simulator robustness

### What SKATR Cannot Do

- **Real observational data:** trained on simulations; would need domain adaptation or retraining on real SKA/HERA data
- **Interpretable parameter extraction directly:** SKATR learns features, not parameters; still need to train downstream task to map representations → parameters
- **Prove simulator-independence:** SKATR generalizes well cross-simulator empirically, but doesn't provide a physical explanation for why (unlike EFT)

## Training Recipe / Getting Started

Based on typical self-supervised ViT workflow:

```python
# Pseudo-code
1. Prepare data: lightcone patches from simulators A, B, ...
2. Initialize ViT encoder + decoder (if MAE) 
3. For each epoch:
    - Sample batch of augmented lightcone patches
    - Forward pass through ViT
    - Compute self-supervised loss (contrastive / MAE / MoCo)
    - Backprop and optimize
4. Save trained encoder
5. For downstream task:
    - Freeze encoder
    - Train MLP on (SKATR_features, label_parameter) pairs
    - Evaluate cross-simulator generalization
```

Code is likely provided in the github repo; check [[Ore et al 2025 (SKATR)]] paper for implementation details.

## For Your Thesis: Why SKATR Matters

### Strategic Value

1. **Proof that simulator-agnostic representations exist:** SKATR demonstrates empirically that neural networks can learn features that generalize across simulators. This validates the general hypothesis underlying the thesis.

2. **Alternative approach to compare against:** the thesis should discuss SKATR as an alternative solution. If the EFT approach outperforms SKATR on interpretability or information content, this is a strong selling point.

3. **Potential collaboration:** if SKATR is available and works well, you could potentially use SKATR-compressed representations as input to P2 inference, enhancing the thesis's scope.

4. **Complementary narrative:** SKATR is the ML-native approach; EFT is the physics-native approach. A thesis that synthesizes both (or at least acknowledges the synergy) is stronger.

### Comparison Points for P2

When writing P2, you might compare:

| Method | Input | Generalization | Interpretability |
|--------|-------|-----------------|------------------|
| EoRFlow (baseline) | 2D power spectrum | Single simulator, poor cross-sim | Medium (native parameters) |
| EoRFlow + SKATR | SKATR latents | Multi-simulator | Medium (need to interpret latents) |
| **P2 EFT** | Power spectrum (or lightcone) | Multi-simulator by construction | **High (EFT coefficients)** |
| SKATR alone | Lightcone | Multi-simulator | Low (black-box) |

If P2 achieves comparable or better cross-simulator performance to SKATR-based inference while maintaining high interpretability (via EFT coefficients), this is a strong validation.

## References and Links

- **Paper:** [[Ore et al 2025 (SKATR)]]
- **Author:** [[Ore, Ayodele]]
- **Related:** [[Inference and ML]], [[Vision Transformer]], [[Self-Supervised Learning]], [[Cross-Simulator Generalization]]
- **Complementary code:** [[EoRFlow]] (downstream inference from SKATR features)
