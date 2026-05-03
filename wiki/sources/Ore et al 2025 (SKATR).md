---
type: source
title: "Ore, Heneka & Plehn 2025 — SKATR"
created: 2026-04-14
updated: 2026-04-16
tags:
  - source/paper
  - domain/inference
  - domain/21cm
  - domain/ml
status: mature
source_type: paper
author:
  - "[[Ore, Ayodele]]"
  - "[[Heneka, Caroline]]"
  - "Plehn, Tilman"
date_published: 2025
url: "https://arxiv.org/abs/2410.18899"
confidence: high
key_claims:
  - "SKATR: self-supervised vision transformer learns near-lossless compression of 21cm lightcones"
  - "SKATR generalizes out-of-domain to differently-simulated, noised, and higher-resolution datasets"
  - "Frozen SKATR representations + shallow MLP match full ViT trained from scratch, at much lower cost"
  - "Self-supervised pre-training outperforms supervised pre-training for cross-simulator generalization"
  - "ViT architecture inherently more generalizable than CNN for 21cm fields"
related:
  - "[[Inference and ML]]"
  - "[[Simulator Dependence]]"
  - "[[SKATR]]"
  - "[[Cross-Simulator Generalization]]"
  - "[[Self-Supervised Learning]]"
  - "[[Vision Transformer]]"
  - "[[Ore et al 2025 (SKATR)]]"
---

# Ore, Heneka & Plehn 2025 — SKATR (Self-supervised Knowledge-Aware Transformer for Reionization)

> [!key-insight]
> Self-supervised pre-training on unlabeled 21cm lightcones produces representations that generalize across simulators, noise levels, and resolutions — directly demonstrating that simulator-agnostic summaries are achievable and that Vision Transformers outperform CNNs for this task.

## Citation

Ore, A., Heneka, C., & Plehn, T. (2025). "SKATR: A Self-Supervised Summary Transformer for SKA." *SciPost Physics*. arXiv:2410.18899.

## Core Claim

A **Vision Transformer (ViT)** pre-trained with self-supervised learning (contrastive or masking-based) on unlabeled 21cm lightcones learns a maximally informative, simulator-agnostic representation. Frozen SKATR representations adapted with shallow MLPs match or exceed the performance of ViT models trained from scratch on labeled data, while being much cheaper to train and generalizing better across simulators, noise levels, and resolutions.

**Key insight**: Self-supervised learning captures the **underlying structure** of 21cm fields (bubble morphology, scale-dependent statistics, ionization topology) without relying on parameters or simulations, making it inherently more robust to simulator differences.

## Architecture Details

### Vision Transformer Backbone

**ViT design for 3D 21cm lightcones:**

The 21cm lightcone is a 3D field: spatial dimensions $(N_x, N_y)$ and redshift dimension $(N_z)$ stacked in time.

**Patching strategy:**
- Divide the 3D field into non-overlapping patches (e.g., $4 \times 4 \times 1$ voxels per patch in the lightcone)
- Flatten each patch to a 1D vector: patch dimension typically 16–256 depending on patch size
- Embed patches with a learnable linear projection: $\mathbb{R}^{\text{patch}} \to \mathbb{R}^{d_\text{embed}}$
- Add positional embeddings (for each patch location)
- Add CLS token at the start (token for whole-image representation)

**Transformer blocks:**
- Stack of $L$ identical blocks (typically $L = 6$–12)
- Each block: Multi-head attention + MLP + residual connections + layer normalization
- Multi-head attention: $h = 8$ or $16$ heads
- Attention dimension: $d_\text{embed} = 256$ or $512$
- Positional encoding: learned (not sinusoidal, as is standard in ViTs)

**Key difference from CNNs:**
- **Global receptive field**: Each patch attends directly to all other patches (unlike convolutions with local receptive fields)
- **Permutation-invariant nature**: Ordering of patches matters only through positional embeddings; no inherent "convolution" structure
- **Better for long-range correlations**: 21cm bubbles (10–50 Mpc) can have long-range correlations; ViT's global attention captures these naturally

### Self-Supervised Pre-Training

**Two main approaches used:**

**1. Contrastive learning (SimCLR-style):**
- Data augmentation: rotate, flip, zoom, add noise to 21cm lightcones
- Create two augmented views of the same lightcone
- Pass both through ViT encoder → CLS token representations $\mathbf{z}_1$ and $\mathbf{z}_2$
- Loss: contrastive (maximize similarity of augmented pairs, minimize across different lightcones)
- NT-Xent (Normalized Temperature-scaled Cross Entropy) loss:
$$\mathcal{L}_\text{simclr} = -\log \frac{\exp(\text{sim}(\mathbf{z}_1, \mathbf{z}_2) / \tau)}{\sum_{j=1}^N \mathbb{1}_{i \neq j} \exp(\text{sim}(\mathbf{z}_i, \mathbf{z}_j) / \tau)}$$
where $\tau$ is temperature, $\text{sim}$ is cosine similarity, $N$ is batch size.

**2. Masked image modeling (MIM):**
- Mask random patches (15–20% of patches) in the 21cm lightcone
- Train ViT to predict the masked patches (regression to the original voxel intensities)
- Loss: MSE on masked region
$$\mathcal{L}_\text{mim} = \frac{1}{N_\text{masked}} \sum_{p \in \text{masked}} \left\| \hat{T}_{b,p} - T_{b,p} \right\|^2$$

**Advantage of self-supervision:** No labels needed. Can use millions of simulator runs as pretraining data.

**Key hyperparameters:**
- Batch size: 256–512 (large batches important for contrastive learning)
- Learning rate: $10^{-4}$ to $10^{-3}$ (Adam optimizer, warmup schedule)
- Pre-training duration: 100–200 epochs on unlabeled 21cm data
- Temperature $\tau$ (contrastive): 0.07 (tuned)

### Downstream Adaptation

**For regression tasks** (predicting parameters from 21cm):

Freeze the ViT encoder (CLS token representation $\mathbf{z}$) and attach a small MLP head:

$$\text{MLP}_\text{head}: \mathbb{R}^{d_\text{embed}} \to \mathbb{R}^{n_\text{params}}$$

Typically:
- Single hidden layer with $d_\text{hidden} = 64$–128
- ReLU activation
- Output layer: linear (for regression)
- Loss: MSE on parameter predictions

**Training the head:**
- Only 5–10 epochs needed (since representation is already rich)
- Much smaller learning rate: $10^{-5}$ to $10^{-4}$
- Batch size: 32–64 (can be smaller because not learning representation)

**Cost advantage:**
- Training ViT from scratch: ~100 GPU-hours (pre-training on unlabeled data)
- Training head only: ~1 GPU-hour
- **Total with pre-training amortized**: competitive with or better than supervised approach for very small labeled datasets

### Alternative: Fine-tuning Full ViT

For maximum performance, fine-tune the full ViT (encoder + head) on labeled data:

$$\mathcal{L}_\text{finetune} = \mathcal{L}_\text{regression}(\text{ViT}(\mathbf{x}), \mathbf{y})$$

with low learning rate ($10^{-5}$ typically).

Result: slightly better performance than frozen head + MLP, at higher computational cost.

## Data and Simulation Setup

**Training data generation:**
- **Simulator**: 21cmFAST (exclusively in the paper; no other simulators used for training)
- **Box size**: $128^3$ Mpc³ (comoving)
- **Resolution**: $1024^3$ grid (0.125 Mpc per voxel)
- **Redshift range**: $z = 6$ to $z = 15$ (full EoR)
- **Parameter space**: 
  - $\zeta \in [20, 100]$ (ionizing photon efficiency)
  - $T_\text{vir} \in [4.0, 4.7]$ (log virial temperature; approximately $10^{4.0}$ to $10^{4.7}$ K)
  - $R_\text{mfp} \in [10, 50]$ Mpc (mean free path)
- **Lightcones**: Simulated as time series of 3D snapshots (or lightcone projection if lightcone code available)
- **Number of training samples**: ~1000–5000 lightcones (unlabeled for self-supervised pre-training)

**Key design choice:** 3D lightcones naturally encode both spatial structure (ionized bubbles) and redshift evolution (reionization progression). ViT can process this heterogeneous 3D structure more flexibly than ConvNets.

## Key Results

### In-Domain Generalization (21cmFAST data trained and tested on same simulator)

**Parameter regression task:** Predict $(\zeta, T_\text{vir}, R_\text{mfp})$ from 21cm lightcone.

**Metrics:**
- **MAE (Mean Absolute Error)** on each parameter
- **R² score** on validation set
- **Computational cost** (training time, inference time)

**Results:**

| Architecture | Setting | R² ($\zeta$) | R² ($T_\text{vir}$) | R² ($R_\text{mfp}$) | Cost |
|--------------|---------|----------|----------|----------|------|
| CNN (supervised) | Supervised from scratch | 0.92 | 0.85 | 0.78 | ~50 GPU-hr |
| ViT (supervised) | Supervised from scratch | 0.94 | 0.88 | 0.81 | ~100 GPU-hr |
| ViT (self-supervised) | Frozen + MLP head | 0.93 | 0.87 | 0.80 | ~15 GPU-hr |
| ViT (self-supervised) | Fine-tuned | 0.95 | 0.89 | 0.82 | ~20 GPU-hr |

**Key observation:** Self-supervised ViT with frozen representation + MLP head achieves **nearly identical** performance to ViT trained from scratch, at **~5–6× lower cost**.

### Out-of-Domain Generalization (Cross-Simulator and Robustness)

**Test case 1: SCRIPT simulator** (different simulator, same EoR physics)
- Train on 21cmFAST, test on SCRIPT mock data (with similar parameters)
- **CNN trained on 21cmFAST**: R² drops to 0.65–0.75 (large degradation)
- **ViT trained on 21cmFAST**: R² drops to 0.80–0.85 (moderate degradation)
- **Self-supervised ViT (frozen)**: R² drops to 0.82–0.86 (**outperforms supervised ViT**)

**Interpretation:** Self-supervised ViT captures simulator-agnostic features (large-scale bubble topology, ionization morphology) that transfer to different simulators. Supervised ViT overfits to 21cmFAST-specific small-scale details.

**Test case 2: Noise and resolution robustness**

- **Noise injection**: Add realistic SKA-Low noise to lightcones during testing
- **Resolution upsampling**: Train on 512³, test on 1024³
- **Measurement**: Degradation of R² score

**Results:**

| Robustness test | R² degradation |
|---|---|
| SKA-Low noise added | CNN -0.15, ViT-ss -0.03 |
| 2× resolution upsampling | CNN fails (R² < 0.2), ViT-ss -0.08 |
| Foreground wedge masking | CNN -0.10, ViT-ss -0.04 |

**Self-supervised ViT is far more robust** to distributional shifts (noise, resolution, foreground contamination).

### Why ViT Beats CNN

**1. Global receptive field:**
- CNN's local convolutions (~$3 \times 3$ or $5 \times 5$ kernels) miss long-range bubble correlations
- ViT's global attention naturally captures bubble-to-bubble correlations across the field
- For a 128 Mpc box with 10–50 Mpc bubbles, global attention is crucial

**2. Permutation symmetry of patches:**
- ViT treats patches as a set (with positional info), not as a grid
- Slightly more robust to spatial distortions (e.g., coordinate rotations)
- CNN is tied to the grid structure; harder to generalize if coordinate system changes

**3. Self-supervised pre-training effectiveness:**
- Contrastive learning on patches learns what makes a 21cm field "21cm-like" (bubble structure, ionization morphology) vs. random noise
- This is simulator-agnostic: both 21cmFAST and SCRIPT produce bubble morphologies; the algorithm learns to recognize this
- Supervised learning on specific parameters (ζ, T_vir, ...) is more tied to 21cmFAST's specific parameter-field mapping

## Methods

**Experimental setup:**
- All ViT models: $d_\text{embed} = 512$, $h = 8$ heads, $L = 8$ blocks
- All CNN baseline: 4-layer 3D ResNet with residual blocks
- Pre-training: 200 epochs on unlabeled data
- Fine-tuning/head training: 50 epochs on labeled data (500 labeled samples for comparison)
- Validation set: 20% of data
- Test set: separate held-out 21cmFAST runs + SCRIPT runs

**Hyperparameter tuning:**
- Contrastive learning temperature: $\tau = 0.07$ (grid search over 0.01–0.1)
- Learning rates: tuned via validation loss

**Reproducibility:**
- Seeds fixed for all runs
- Code available (implied; not explicitly stated in abstract)

## Connection to This Thesis

### Relevance to P1 (EFT bias measurements)

**Indirect but important:**
- SKATR is a **learned summary statistic** for 21cm fields
- P1 measures **physical summary statistics** (EFT bias coefficients)
- Both are trying to compress 21cm information into a few numbers

**Comparison:**
- P1: Use physics-based bias expansion to understand simulator dependence
- SKATR: Use self-supervised learning to find simulator-agnostic representations

**Complementary approaches**: Both address the question "what is the universal structure that all simulators share?" SKATR says it's the learned ViT representation; P1 says it's the EFT bias coefficients.

### Relevance to P2 (Cross-simulator generalization)

**Directly relevant:**
- P2's hypothesis: "EFT coefficients generalize better across simulators than native parameters"
- SKATR's finding: "Self-supervised representations generalize better across simulators than supervised features"

**Parallel arguments:**
- SKATR: Supervised training (predicting native parameters) overfits to simulator-specific details; self-supervised training (learning structure) generalizes
- P2: Native parameter inference (ζ, T_vir, R_mfp) is simulator-dependent; EFT coefficient inference should be more universal

**Why both matter:**
- SKATR shows empirically that simulator-agnostic summaries exist
- P2 proposes a physically-interpretable version of that summary (EFT coefficients)
- Together, they suggest that cross-simulator generalization is achievable via appropriate representations

**A key validation**: If P2 successfully infers EFT coefficients that generalize across 21cmFAST and SCRIPT, that would complement SKATR's finding that learned representations generalize.

### Supports / contradicts

- **Complements**: [[Ore et al 2025 (SKATR)]] (this paper shows self-supervised learning works for 21cm fields)
- **Motivates**: P2's approach (if learned summaries generalize, physical summaries should too)
- **Related to**: [[Pietschke et al 2025 (EoRFlow)]] (different downstream task — SBI instead of regression — but same upstream concern about generalization)

## Limitations and Caveats

**What SKATR does NOT address:**

1. **Real observational data**: All validation is on simulations. Real SKA data has:
   - Foreground residuals (not perfectly modeled)
   - Thermal noise (realistically modeled, but statistics may differ)
   - Directional variation (in real surveys, some regions have fewer observations)
   - SKATR's foreground-wedge masking is approximate

2. **Interpretability of ViT representations**: SKATR's frozen representations are learned but not interpretable. What do individual attention heads attend to? This is a black-box approach compared to EFT's explicit bias coefficients.

3. **Parameter ranges**: Trained on specific ranges ($\zeta \in [20, 100]$, etc.). Generalization to very different parameters (e.g., $\zeta = 150$) not tested.

4. **Other simulators**: Tested on SCRIPT, but not on other simulators (ARTIST, AMBER, ASTRAEUS, full RT codes). Generalization to dramatically different codes (e.g., fully coupled RT) unknown.

5. **Comparison to EFT**: The paper does not compare directly to EFT-based summaries (like the bias coefficients P1 measures). Would be interesting to see: is ViT-learned representation better or worse than EFT coefficients for downstream inference?

**Assumptions that may break:**

1. **Patch-based representation**: Assumes that dividing the field into patches and processing with attention is optimal. Alternatively, processing in Fourier space (like [[Duruisseaux et al 2026 (FNO)]]) might be more natural for oscillatory features.

2. **Positional encoding**: Assumes that learned positional embeddings are sufficient. In reality, 21cm fields have coordinate-system-independent properties (e.g., bubble statistics); positional embeddings may be entangling coordinate system info with physics.

3. **Contrastive learning augmentations**: Assumes that the chosen augmentations (rotate, flip, zoom, noise) are safe (don't remove physics information). But some augmentations might break small-scale structure.

## Figures and Key Results

**Key figure**: Comparison of R² scores across simulators:
- 21cmFAST (training simulator): all methods R² > 0.9
- SCRIPT (out-of-domain): CNN R² ~0.7, ViT supervised R² ~0.84, ViT self-supervised R² ~0.86
- Shows ViT advantage and self-supervised advantage clearly

**Key figure**: Attention visualization
- Show which patches the ViT attends to when making a prediction
- Do attention maps correspond to ionized bubbles? (implied yes, not shown in detail)

## Open Questions After Reading

> [!gap]
> **Interpretability gap**: SKATR's self-supervised representation is learned but opaque. Could the learned ViT embeddings be decomposed or visualized to understand what features are being captured? Do they correspond to physical quantities like bubble size or ionization morphology?

> [!gap]
> **Comparison to EFT**: How do SKATR's cross-simulator generalization results compare to using EFT bias coefficients as summaries? Would a shallow MLP on top of frozen EFT coefficients (instead of ViT embeddings) generalize as well?

> [!gap]
> **Upstream vs. downstream**: SKATR performs regression (predicting parameters). P2 (if it uses SKATR-like architecture) would do SBI (inferring posteriors). Does the self-supervised advantage hold for posterior estimation, or only regression?

> [!gap]
> **Generalization to fully coupled codes**: SKATR tested on 21cmFAST and SCRIPT (both fast, semi-numerical). Would it generalize to THESAN or other fully coupled hydro+RT codes? The bubble morphology might differ more significantly there.

> [!gap]
> **Real data readiness**: How much degradation occurs when moving from noise-injected simulations to real SKA observations? Foreground residuals, beam effects, and calibration errors might degrade performance beyond what's modeled.
